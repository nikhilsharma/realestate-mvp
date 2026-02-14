from app.db import get_db_connection

def create_client(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clients
        (name, contact, requirement, property_type, location, budget, followup_date, status, notes, next_action)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["name"],
        data["contact"],
        data["requirement"],
        data["property_type"],
        data["location"],
        data["budget"],
        data["followup_date"],
        "Active",
        data["notes"],
        data["next_action"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results