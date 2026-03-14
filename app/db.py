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

    cursor.execute("""
    ALTER TABLE clients
    ADD COLUMN IF NOT EXISTS location_normalized TEXT
    """)

    cursor.execute("""
    ALTER TABLE clients
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
    """)

    cursor.execute("""
    ALTER TABLE properties
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
    """)

    cursor.execute("""
    ALTER TABLE clients
    ADD COLUMN IF NOT EXISTS lead_score INTEGER DEFAULT 0,
    ADD COLUMN IF NOT EXISTS lead_temperature VARCHAR(10) DEFAULT 'cold',
    ADD COLUMN IF NOT EXISTS last_contacted_at TIMESTAMP NULL;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS broker_properties (
            id SERIAL PRIMARY KEY,
            area_cluster TEXT NOT NULL,
            location TEXT NOT NULL,
            location_normalized TEXT,
            budget INTEGER NOT NULL,
            mode TEXT CHECK (mode IN ('Rent','Sale')),
            type TEXT DEFAULT 'Residential',
            video_link TEXT,
            broker_name TEXT,
            broker_contact TEXT,
            tags TEXT[],
            is_available BOOLEAN DEFAULT TRUE,
            last_confirmed_at DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
    ALTER TABLE broker_properties
    ADD COLUMN IF NOT EXISTS configuration TEXT
    """)

    cursor.execute("""
    ALTER TABLE broker_properties
    ADD COLUMN IF NOT EXISTS whatsapp_video_ref TEXT;
    """)

    cursor.execute("""
    ALTER TABLE clients
    ADD COLUMN IF NOT EXISTS lead_temperature_override TEXT
    """)

    cursor.execute("""
    ALTER TABLE broker_properties
    ADD COLUMN IF NOT EXISTS owner_name TEXT,
    ADD COLUMN IF NOT EXISTS owner_contact TEXT;
    """)

    cursor.execute("""
    ALTER TABLE broker_properties
    ADD COLUMN IF NOT EXISTS area INTEGER
    """)

    conn.commit()
    cursor.close()
    conn.close()