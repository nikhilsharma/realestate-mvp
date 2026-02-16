import psycopg2
import time
from config import Config

def get_db_connection(retries=3, delay=2):
    for attempt in range(retries):
        try:
            return psycopg2.connect(Config.DATABASE_URL)
        except psycopg2.OperationalError as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
            
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            name TEXT,
            contact TEXT,
            requirement TEXT,
            property_type TEXT,
            location TEXT,
            budget INTEGER,
            followup_date DATE,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        ALTER TABLE clients
        ADD COLUMN IF NOT EXISTS notes TEXT
    """)

    cursor.execute("""
        ALTER TABLE clients
        ADD COLUMN IF NOT EXISTS next_action TEXT
    """)

    cursor.execute("""
    ALTER TABLE properties
    ADD COLUMN IF NOT EXISTS video_link TEXT
    """)

    cursor.execute("""
    ALTER TABLE properties
    ADD COLUMN IF NOT EXISTS dealer_name TEXT
    """)

    cursor.execute("""
        ALTER TABLE properties
        ADD COLUMN IF NOT EXISTS dealer_contact TEXT
    """)

    cursor.execute("""
    ALTER TABLE clients
    ADD COLUMN IF NOT EXISTS profession TEXT
    """)


    conn.commit()
    cursor.close()
    conn.close()