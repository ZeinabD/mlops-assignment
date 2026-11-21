
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

# Load the trained model downloaded from DagsHub
model = joblib.load("model/model.joblib")

# Create FastAPI application
# Disable automatic documentation routes so /predict is the only endpoint.
app = FastAPI(
    title="Digit Prediction API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


# Define the expected input
class PredictionInput(BaseModel):
    pixels: list[int] = Field(min_length=64, max_length=64)


# The only API endpoint
@app.post("/predict")
def predict(data: PredictionInput):

    # Check that pixel values are between 0 and 16
    if any(pixel < 0 or pixel > 16 for pixel in data.pixels):
        raise HTTPException(
            status_code=400,
            detail="Pixel values must be between 0 and 16."
        )

    # Convert input into the format expected by Scikit-learn
    input_data = np.array(data.pixels).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)

    return {
        "predicted_digit": int(prediction[0])
    }
