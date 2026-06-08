# 💸 AI Expense Categoriser

A machine‑learning powered tool that automatically classifies transaction descriptions into spending categories.  
The project combines a FastAPI backend, a Streamlit frontend, and a production‑ready scikit‑learn pipeline.

---

## 🚀 Features

### **Real‑time categorisation**
Enter a transaction description and instantly receive:
- Predicted category  
- Confidence score  
- Full probability breakdown  

### **Batch CSV processing**
Upload a CSV file and get:
- Category predictions for each row  
- Confidence scores  
- A category distribution chart  

### **Interactive visualisations**
The UI includes:
- Colour‑coded probability bars  
- Category distribution analytics  
- Session‑based prediction history  

### **Improved ML pipeline**
The model uses:
- Text cleaning  
- TF‑IDF vectorisation with unigrams and bigrams  
- Stopword removal  
- Logistic Regression tuned for imbalanced data  
- A unified scikit‑learn Pipeline for clean deployment  

---

## ⚙️ How It Works

### **1. Training**
The model is trained on a dataset of transaction descriptions and categories.  
The training pipeline handles:

- Lowercasing  
- Removing punctuation and numbers  
- TF‑IDF vectorisation  
- Logistic Regression classification  

The final model is saved as a single `.pkl` file for easy loading.

### **2. Backend (FastAPI)**
The API exposes a `/categorise` endpoint that accepts:

```json
{ "description": "Tesco £12.50" }
