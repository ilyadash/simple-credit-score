import joblib
import sys
import os
from contextlib import asynccontextmanager
from io import StringIO, BytesIO
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.testclient import TestClient
from fastapi.responses import StreamingResponse
from src.db import insert_credit_record, init_db, bulk_insert_credit_records
from src.my_processor import MyDataPreprocessor

# Add the app directory to Python path to resolve module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.model = joblib.load(
        "/app/model/credit_default_pipeline.joblib"
    )
    yield

app = FastAPI(debug=True, lifespan=lifespan)

from src.schemas import CreditRecord, PredictionOut, CreditFile
import pandas as pd

@app.get("/test")
async def test(name: str = "Guest"):
    return {"message": f"Hello, {name} ! The server test is success!"}

async def predict_from_dataframe(X: pd.DataFrame):
    if 'loan_status' in X.columns:
        X = X.drop(columns='loan_status')
    probabilities = app.state.model.predict_proba(X)[:,0]
    answers = app.state.model.predict(X)
    return {"default_probability": float(probabilities), "expected_default": int(answers)}

@app.post("/predict_one")
async def predict(data: CreditRecord):
    X = pd.DataFrame([data.model_dump()])
    if 'loan_status' in X.columns:
        X = X.drop(columns='loan_status')
    probability = app.state.model.predict_proba(X)[0, 1]
    answer = app.state.model.predict(X)
    return {"default_probability": float(probability), "expected_default": int(answer)}

@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    # 1. Читаем входящий файл в Pandas
    contents = await file.read()
    provided_data = pd.read_csv(BytesIO(contents)) # Используем BytesIO, так как UploadFile.file — это бинарный поток
    X = provided_data.copy(deep=True)
    # 2. Подготавливаем данные перед подачей в модель
    if 'loan_status' in X.columns:
        X = X.drop(columns='loan_status')
    # 3. Делаем предсказание
    probability = app.state.model.predict_proba(X)[:, 1]
    answer = app.state.model.predict(X)
    probs_and_predictions = pd.DataFrame()
    probs_and_predictions['default_probability'] = pd.Series(probability)
    probs_and_predictions['pred_class'] = pd.Series(answer)
    # 4. Сохраянем данные по кредиту и предсказанию для него в базу
    processed_data = provided_data.copy(deep=True)
    processed_data['default_probability'] = pd.Series(probability)
    processed_data['pred_class'] = pd.Series(answer)
    bulk_insert_credit_records(processed_data)
    # 5. Подготовка ответа без сохранения на диск
    stream = StringIO()
    probs_and_predictions.to_csv(stream, index=False)
    
    # 6. Создаем ответ и добавляем заголовки для скачивания
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename=prediction_{file.filename}"
    return response

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/load_data_from_csv")
async def load_data_from_csv(payload: UploadFile = File(...)):
    X = pd.read_csv(payload)
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
