import joblib
from fastapi import FastAPI

app = FastAPI()

from app.src.schemas import CreditRecordIn, PredictionOut
from app.src.db import insert_credit_record, init_db

@app.on_event("startup")
def startup():
    init_db()

@app.on_event("startup")
def load_model():
    app.state.model = joblib.load(
        "credit_default_pipeline.joblib"
    )

import pandas as pd

@app.post("/predict")
def predict(payload: dict):
    X = pd.DataFrame([payload])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
