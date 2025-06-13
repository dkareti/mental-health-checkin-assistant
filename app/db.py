import sqlite3
import datetime

DB_FILE = "data/mood_logs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            user_input TEXT,
            sentiment TEXT,
            score REAL
        )
    """)
    conn.commit()
    conn.close()

def log_mood(text, sentiment, score):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (date, user_input, sentiment, score) VALUES (?, ?, ?, ?)",
                   (datetime.date.today().isoformat(), text, sentiment, score))
    conn.commit()
    conn.close()

def get_weekly_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    seven_days_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    cursor.execute("SELECT sentiment FROM logs WHERE date >= ?", (seven_days_ago,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "I don't have enough data to summarize your week. Let's start tracking today."

    sentiments = [row[0] for row in rows]
    summary = {
        "positive": sentiments.count("positive"),
        "neutral": sentiments.count("neutral"),
        "negative": sentiments.count("negative")
    }

    return (f"Here's your mood summary for the past week: 😊 {summary['positive']} positive days, 😐 {summary['neutral']} neutral, 😔 {summary['negative']} tough days. "
            f"You're doing your best — let's keep going one day at a time!")