import sqlite3
import json
DB_NAME = "news_emotions.db.sqlite"

def init_db():
    server = sqlite3.connect(DB_NAME)
    cursor = server.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,
        headline TEXT,
        summary TEXT,
        emotion TEXT,
        entities TEXT,
        url TEXT,
        source TEXT,
        UNIQUE(datetime, headline)
    )
    """)
    server.commit()
    server.close()
def insert_new(datetime , headline , summary , emotion , entities , url , source):
    server = sqlite3.connect(DB_NAME)
    cursor = server.cursor()
    try:
        entities_str = json.dumps(entities) if isinstance(entities, (list, dict)) else str(entities)
        cursor.execute("""
        INSERT INTO news (datetime, headline, summary, emotion, entities, url, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime, headline, summary, emotion, entities_str, url, source))
    except sqlite3.IntegrityError:
        pass
    server.commit()
    server.close()
def fetchrows():
    server = sqlite3.connect(DB_NAME)
    cursor = server.cursor()
    cursor.execute("SELECT * FROM news ORDER BY datetime DESC")
    rows = cursor.fetchall()
    server.close()
    return rows

    
    
