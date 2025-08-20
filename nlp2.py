from scraper_vc import fetch_news
from emotional_classifier import classify_emotion
from ner import extract_entities
from datetime import datetime
from db_connect import init_db , insert_new

init_db()

news_articles = fetch_news("general")

for article in news_articles:
    summary = article.get("summary" , "")
    headline = article.get("headline" , "")

    if not summary or not  headline:
        continue

    emotion = classify_emotion(summary)
    entity = extract_entities(summary)

    insert_new(datetime.utcfromtimestamp(article["datetime"]).strftime('%Y-%m-%d %H:%M:%S') , headline , summary , emotion , entity , article.get("url" , "") , article.get("source" , "")) 

