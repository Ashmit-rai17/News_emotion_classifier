import streamlit as st
import os
from stock_utils import get_stock_price

# --- TRY LOADING EMOTION MODEL SAFELY ---
MODEL_READY = False
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    model_name = "j-hartmann/emotion-english-distilroberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    labels = model.config.id2label
    MODEL_READY = True
except Exception as e:
    st.warning(f"⚠️ Could not load emotion model (likely memory limit). App will still run.\n\nError: {e}")


# --- EMOTION CLASSIFICATION FUNCTION ---
def classify_emotion(text: str) -> str:
    if not MODEL_READY:
        return "Model not available"
    inputs = tokenizer([text], return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_idx = torch.argmax(prediction, dim=-1).item()
    return labels[pred_idx]


# --- STREAMLIT APP START ---
st.set_page_config(page_title="News Emotion Classifier", layout="wide")

# Sidebar with stock prices
st.sidebar.header("📈 Live Stock Prices")
companies = {
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Meta": "META"
}

for name, symbol in companies.items():
    price, change = get_stock_price(symbol)
    if price == "N/A":
        st.sidebar.write(f"{name}: N/A")
    else:
        arrow = "🟢⬆️" if change >= 0 else "🔴⬇️"
        st.sidebar.write(f"{name}: {price:.2f} {arrow}")


# Main section
st.title("📰 News Emotion Classifier")

user_input = st.text_area("Enter a news headline:")
if st.button("Classify Emotion"):
    if user_input.strip():
        emotion = classify_emotion(user_input)
        st.success(f"Predicted Emotion: **{emotion}**")
    else:
        st.error("Please enter some text.")
