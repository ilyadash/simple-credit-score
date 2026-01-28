import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.testclient import TestClient
from src.db import insert_credit_record, init_db

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

@app.post("/predict")
async def predict(data: CreditRecord):
    X = pd.DataFrame([data.model_dump()])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/load_data_from_csv")
async def load_data_from_csv(payload: dict):
    X = pd.DataFrame([payload])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
