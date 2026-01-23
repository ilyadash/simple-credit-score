import joblib
from fastapi import FastAPI, File, UploadFile

app = FastAPI(debug=True)

from app.src.schemas import CreditRecordIn, PredictionOut
from app.src.db import insert_credit_record, init_db

@app.on_event("startup")
def startup():
    init_db()

@app.on_event("startup")
def load_model():
    app.state.model = joblib.load(
        "/model/credit_default_pipeline.joblib"
    )

import pandas as pd

@app.post("/predict")
def predict(payload: dict):
    X = pd.DataFrame([payload])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/load_data_from_csv")
def load_data_from_csv(payload: dict):
    X = pd.DataFrame([payload])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
