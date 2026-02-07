import streamlit as st
import requests

st.set_page_config(page_title="Car Price Predictor")

st.title("Car Price Prediction")
st.write("Enter vehicle details to estimate the resale price.")


col1, col2 = st.columns(2)

with col1:
    manufacturer = st.selectbox(
        "Manufacturer",
        ["Ford", "Toyota", "BMW", "Audi", "Honda", "Hyundai"]
    )

    fuel_type = st.selectbox(
        "Fuel Type",
        ["Petrol", "Diesel", "Hybrid"]
    )

    engine_size = st.number_input(
        "Engine Size (L)",
        min_value=0.5,
        max_value=6.0,
        step=0.1,
        value=1.5
    )

with col2:
    model = st.text_input("Model", "Focus")

    year = st.number_input(
        "Year of Manufacture",
        value=2015
    )

    mileage = st.number_input(
        "Mileage (km)",
        min_value=0,
        max_value=300000,
        value=50000
    )

st.divider()

if st.button("Predict Price"):

    errors = []

    if manufacturer.strip() == "":
        errors.append("Manufacturer")

    if model.strip() == "":
        errors.append("Model")

    if fuel_type.strip() == "":
        errors.append("Fuel Type")

    if engine_size <= 0:
        errors.append("Engine Size")

    if year <= 1900:
        errors.append("Year of Manufacture")

    if mileage < 0:
        errors.append("Mileage")

    # If validation fails
    if errors:
        st.warning(f"Please enter valid values for: {', '.join(errors)}")

    else:
        payload = {
            "manufacturer": manufacturer,
            "model": model,
            "engine_size": engine_size,
            "fuel_type": fuel_type,
            "year_of_manufacture": year,
            "mileage": mileage
        }

        try:
            with st.spinner("Predicting price..."):
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload
                )

            if response.status_code == 200:
                price = response.json()["predicted_price"]
                st.metric("Estimated Price", f"₹ {price:,.0f}")
            else:
                st.error("API returned an error.")

        except requests.exceptions.ConnectionError:
            st.error("API is not running.")

