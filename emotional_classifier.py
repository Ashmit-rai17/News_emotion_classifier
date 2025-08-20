import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "j-hartmann/emotion-english-distilroberta-base"  # Roberta model for emotion classification
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def classify_emotion(data: str) -> str:
    """
    Classify the emotion of a given text string using the RoBERTa model.
    """
    inputs = tokenizer([data], return_tensors="pt", truncation=True, padding=True)  # wrap in list
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_idx = torch.argmax(prediction, dim=-1).item()
    labels = model.config.id2label
    return labels[pred_idx]
