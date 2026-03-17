from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import logging

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# -------------------------
# Load Model and Vectorizer
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(BASE_DIR, "models", "spam_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

logger.info("Model and vectorizer loaded successfully")

# -------------------------
# Request Schema
# -------------------------
class Message(BaseModel):
    text: str

# -------------------------
# Home Route
# -------------------------
@app.get("/")
def home():
    return {"message": "Spam Detection API is running"}

# -------------------------
# Prediction Endpoint
# -------------------------
@app.post("/predict")
def predict(data: Message):

    message = data.text.strip()

    # Input validation
    if not message:
        logger.warning("Empty message received")
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Received message: {message}")

    # Vectorize input
    vector = vectorizer.transform([message])

    # Predict
    prediction = model.predict(vector)[0]

    result = "Spam" if prediction == 1 else "Ham"

    logger.info(f"Prediction result: {result}")

    return {"prediction": result}