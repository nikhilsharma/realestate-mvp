from app.db import get_db_connection
from app.services.matching import build_location_filter
from app.services.client_rules import map_client_requirement_to_property_mode

def create_property(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO properties
        (type, mode, location, budget, area, owner_name, owner_contact, status, dealer_name, dealer_contact, video_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["type"],
        data["mode"],
        data["location"],
        data["budget"],
        data["area"],
        data["owner_name"],
        data["owner_contact"],
        "Available",
        data.get("dealer_name"),
        data.get("dealer_contact"),
        data["video_link"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

def get_properties(search=None, mode=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM properties WHERE is_active = TRUE AND status = 'Available'"
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

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return results

def toggle_property_status(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE properties
        SET status = CASE
            WHEN status = 'Available' THEN 'Closed'
            ELSE 'Available'
        END
        WHERE id = %s
    """, (property_id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_matching_properties(client):
    conn = get_db_connection()
    cursor = conn.cursor()

    mode = map_client_requirement_to_property_mode(client.get("requirement"))

    if not mode:
        cursor.close()
        conn.close()
        return []

    query = """
        SELECT * FROM properties
        WHERE mode = %s
        AND type = %s
        AND is_active = TRUE
        AND status = 'Available'
    """
    params = [mode, client["property_type"]]

    # Location filter
    if client["location"]:
        location_sql, location_params = build_location_filter(client.get("location"))
        query += location_sql
        params.extend(location_params)

    # Budget filter (±10%)
    if client["budget"]:
        lower = int(client["budget"] * 0.9)
        upper = int(client["budget"] * 1.1)
        query += " AND budget BETWEEN %s AND %s"
        params.extend([lower, upper])

    query += " ORDER BY created_at DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

def get_property_by_id(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties WHERE id = %s", (property_id,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return None

    columns = [desc[0] for desc in cursor.description]
    result = dict(zip(columns, row))

    cursor.close()
    conn.close()

    return result

def update_property(property_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE properties
        SET type=%s,
            mode=%s,
            location=%s,
            budget=%s,
            area=%s,
            owner_name=%s,
            owner_contact=%s,
            dealer_name=%s,
            dealer_contact=%s,
            video_link=%s
        WHERE id=%s
    """, (
        data["type"],
        data["mode"],
        data["location"],
        data["budget"],
        data["area"],
        data["owner_name"],
        data["owner_contact"],
        data.get("dealer_name"),
        data.get("dealer_contact"),
        data["video_link"],
        property_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

def soft_delete_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE properties
        SET is_active = FALSE
        WHERE id = %s
    """, (property_id,))

    conn.commit()
    cursor.close()
    conn.close()