import joblib
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def load_model():
    app.state.model = joblib.load(
        "credit_default_pipeline.joblib"
    )

from app.src.db import engine
from app.src import models

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

import pandas as pd

@app.post("/predict")
def predict(payload: dict):
    X = pd.DataFrame([payload])
    proba = app.state.model.predict_proba(X)[0, 1]
    return {"default_probability": float(proba)}
