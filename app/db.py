import psycopg2
from config import Config

def get_db_connection():
    return psycopg2.connect(Config.DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
            type TEXT,
            mode TEXT,
            location TEXT,
            budget INTEGER,
            area INTEGER,
            owner_name TEXT,
            owner_contact TEXT,
            status TEXT DEFAULT 'Available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()