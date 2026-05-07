from fastapi import FastAPI
import joblib
import numpy as np
import json

model = joblib.load("model.pkl")

with open("metrics.json") as f:
    metrics = json.load(f)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "MLOps Pipeline Running"}

@app.get("/metrics")
def get_metrics():
    return metrics

@app.post("/predict")
def predict(data: dict):
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0]
    return {"prediction": int(prediction)}
