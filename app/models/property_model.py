from app.db import get_db_connection

def create_property(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO properties
        (type, mode, location, budget, area, owner_name, owner_contact)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["type"],
        data["mode"],
        data["location"],
        data["budget"],
        data["area"],
        data["owner_name"],
        data["owner_contact"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

def get_all_properties():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties ORDER BY created_at DESC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data