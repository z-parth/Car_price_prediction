from fastapi import FastAPI
import pandas as pd
import joblib
from pathlib import Path
from app.schemas import CarInput

# Initialize app
app = FastAPI(title="Car Price Prediction API")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "artifacts" / "models" / "car_price_pipeline.pkl"

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
preprocessor = bundle["preprocessor"]

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/predict")
def predict(car: CarInput):
    
    df = pd.DataFrame([car.dict()])

    # Preprocess
    X = preprocessor.transform(df)

    # Predict
    price = model.predict(X)[0]

    return {
        "predicted_price": float(price)
    }
print(preprocessor.feature_names_in_)

