import sqlite3

def init_db():
    conn = sqlite3.connect("insights.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            prompt TEXT,
            insights TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_insight_to_db(file_name, prompt, insights):
    conn = sqlite3.connect("insights.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO insights (file_name, prompt, insights)
        VALUES (?, ?, ?)
    """, (file_name, prompt, insights))
    conn.commit()
    conn.close()

def load_all_insights():
    conn = sqlite3.connect("insights.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM insights ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return records
