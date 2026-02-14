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

def get_properties(search=None, mode=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if search and search.strip():
        search = search.strip()
        query += " AND (location ILIKE %s OR owner_name ILIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if mode and mode.strip():
        mode = mode.strip()
        query += " AND mode = %s"
        params.append(mode)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results