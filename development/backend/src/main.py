import joblib
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.testclient import TestClient
from src.db import insert_credit_record, init_db
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

from src.schemas import CreditRecord, PredictionOut
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
async def predict_file(data):
    X = pd.DataFrame([data.model_dump()])
    if 'loan_status' in X.columns:
        X = X.drop(columns='loan_status')
    probability = app.state.model.predict_proba(X)[:, 1]
    answer = app.state.model.predict(X)
    probs_and_predictions = pd.DataFrame()
    probs_and_predictions['default_probability'] = pd.Series(probability)
    probs_and_predictions['pred_class'] = pd.Series(answer)
    return probs_and_predictions.to_csv(path_or_buf=None)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/load_data_from_csv")
async def load_data_from_csv(payload: UploadFile = File(...)):
    X = pd.read_csv(payload)
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
