import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# -------------------------
# Text Cleaning Function
# -------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)  # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip()  # normalise whitespace
    return text

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("data/transactions.csv")

# Clean descriptions
df["description"] = df["description"].astype(str).apply(clean_text)

# -------------------------
# Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["description"],
    df["category"],
    test_size=0.2,
    random_state=42,
    stratify=df["category"]  # ensures balanced split
)

# -------------------------
# Build Pipeline
# -------------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),       # unigrams + bigrams
        stop_words="english",     # remove noise
        min_df=2,                 # ignore rare words
        max_df=0.9                # ignore overly common words
    )),
    ("clf", LogisticRegression(
        max_iter=300,
        C=2.0,
        class_weight="balanced"   # handles class imbalance
    ))
])

# -------------------------
# Train model
# -------------------------
pipeline.fit(X_train, y_train)

# -------------------------
# Evaluate
# -------------------------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy:.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------
# Save model
# -------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, "models/expense_model.pkl")

print("Saved improved model to models/expense_model.pkl")
