import streamlit as st
import requests

st.title("Car Price Predictor")

manufacturer = st.text_input("Manufacturer")
model = st.text_input("Model")
engine_size = st.number_input("Engine Size", value=1.0)
fuel_type = st.text_input("Fuel Type")
year = st.number_input("Year of Manufacture", value=2015)
mileage = st.number_input("Mileage", value=50000)

if st.button("Predict Price"):
    payload = {
        "manufacturer": manufacturer,
        "model": model,
        "engine_size": engine_size,
        "fuel_type": fuel_type,
        "year_of_manufacture": year,
        "mileage": mileage
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    if response.status_code == 200:
        st.success(f"Predicted Price: {response.json()['predicted_price']}")
    else:
        st.error("Prediction failed")
