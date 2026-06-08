from fastapi import FastAPI
import joblib

app = FastAPI()

# Load model + vectorizer
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

@app.get("/")
def home():
    return {"message": "AI Expense Categoriser API is running"}

@app.post("/categorise")
def categorise(transaction: dict):
    description = transaction["description"]

    # Vectorise
    vec = vectorizer.transform([description])

    # Predict category
    prediction = model.predict(vec)[0]

    # Predict probabilities
    probs = model.predict_proba(vec)[0]

    # Map probabilities to category names
    categories = model.classes_
    confidence = {cat: float(prob) for cat, prob in zip(categories, probs)}

    # Highest confidence score
    top_confidence = float(max(probs))

    return {
        "category": prediction,
        "confidence": top_confidence,
        "all_confidences": confidence
    }
