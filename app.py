import streamlit as st
import json
from datetime import datetime
from db_connect import fetchrows
from stock_utils import get_stock_price

st.set_page_config(page_title="VC News Sentiment", layout="wide")

st.markdown(
    """
    <style>
        .headline-card {
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            color: #2c3e50;
        }
        .headline-title {
            font-size: 18px;
            font-weight: bold;
        }
        .meta {
            font-size: 14px;
            color: #555;
        }
        .emotion-tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            color: white;
        }
        .positive { background-color: #27ae60; }
        .negative { background-color: #e74c3c; }
        .neutral { background-color: #95a5a6; }
        .joy { background-color: #f1c40f; } 
        .sadness { background-color: #3498db; } 
        .fear { background-color: #9b59b6; } 
        .anger { background-color: #e67e22; } 
        .surprise { background-color: #1abc9c; } 
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 News Sentiment & Stock Correlation")

rows = fetchrows()

st.sidebar.header("🔍 Filters")

all_entities = []
for row in rows:
    _, _, _, _, _, entities, _, _ = row
    entities = json.loads(entities) if entities else []
    for ent in entities:
        if isinstance(ent, dict):
            for label, value in ent.items():
                if label == "ORG":
                    all_entities.append(value)

all_entities = sorted(list(set(all_entities)))

selected_entity = st.sidebar.selectbox("Select Company", ["All"] + all_entities)
selected_emotion = st.sidebar.selectbox("Select Emotion", ["All", "Positive", "Negative", "Neutral", "Joy", "Sadness", "Fear", "Anger", "Surprise"])
date_range = st.sidebar.date_input("Select Date Range", [])

st.sidebar.header("Live Stock Prices")
famous_companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google (Alphabet)": "GOOGL",
    "Meta (Facebook)": "META",
    "Netflix": "NFLX",
    "NVIDIA": "NVDA"
}
for name , ticker in famous_companies.items():
    price , change , trend = get_stock_price(ticker)
    if price:
        if trend == "up":
            st.sidebar.markdown(f"**{name} ({ticker})**: <span style='color:green;'>${price} 📈 (+{change})</span>", unsafe_allow_html=True)
        elif trend == "down":
            st.sidebar.markdown(f"**{name} ({ticker})**: <span style='color:red;'>${price} 📉 ({change})</span>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"**{name} ({ticker})**: ${price} ➖ (0.00)")
    else:
        st.sidebar.write(f"**{name} ({ticker})**: N/A")

for row in rows:
    _, dt, headline, summary, emotion, entities, url, source = row
    entities = json.loads(entities) if entities else []

    emotion_class = "neutral"
    if "pos" in emotion.lower():
        emotion_class = "positive"
    elif "neg" in emotion.lower():
        emotion_class = "negative"
    elif "joy" in emotion.lower():
        emotion_class = "joy"
    elif "sad" in emotion.lower():
        emotion_class = "sadness"
    elif "fear" in emotion.lower():
        emotion_class = "fear"
    elif "ang" in emotion.lower():
        emotion_class = "anger"
    elif "surp" in emotion.lower():
        emotion_class = "surprise"

    show_row = True

    if selected_entity != "All":
        orgs_in_row = [ent.get("ORG") for ent in entities if isinstance(ent, dict) and "ORG" in ent]
        if selected_entity not in orgs_in_row:
            show_row = False

    if selected_emotion != "All":
        if selected_emotion.lower() not in emotion.lower():
            show_row = False

    if date_range:
        try:
            dt_parsed = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").date()
            if not (date_range[0] <= dt_parsed <= date_range[-1]):
                show_row = False
        except:
            pass

    if not show_row:
        continue

    with st.container():
        st.markdown(f"""
            <div class="headline-card {emotion_class}">
                <div class="headline-title">{headline}</div>
                <div class="meta">{dt} | {source} | <a href="{url}" target="_blank">Read More</a></div>
                <p>{summary}</p>
                <span class="emotion-tag {emotion_class}">{emotion}</span>
            </div>
        """, unsafe_allow_html=True)

        orgs = []
        for ent in entities:
            if isinstance(ent, dict) and "ORG" in ent:
                orgs.append(ent["ORG"])

        if orgs:
            st.write("**Entities:**", ", ".join(orgs))
        
