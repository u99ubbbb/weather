import sqlite3
from datetime import datetime

DB_NAME = "weather.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            weather TEXT,
            max_temp REAL,
            min_temp REAL,
            humidity INTEGER,
            wind_speed REAL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_weather(city, weather):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weather_history
        (city, weather, max_temp, min_temp, humidity, wind_speed, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        city,
        weather["weather"],
        weather["max_temp"],
        weather["min_temp"],
        weather["humidity"],
        weather["wind_speed"],
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()


def get_history(city):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM weather_history
        WHERE city = ?
        ORDER BY created_at DESC
    """, (city,))

    rows = cur.fetchall()
    conn.close()

    return rows