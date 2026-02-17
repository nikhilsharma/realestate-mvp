from app.db import get_db_connection
from datetime import date
from app.services.location_utils import normalize_location
from app.services.seller_matching import filter_matching_buyers

def create_client(data):
    location_normalized = normalize_location(data.get("location"))
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clients
        (name, contact, requirement, property_type, location, location_normalized, budget, followup_date, status, notes, next_action, profession)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["name"],
        data["contact"],
        data["requirement"],
        data["property_type"],
        data["location"],
        location_normalized,
        data["budget"],
        data["followup_date"],
        "Active",
        data["notes"],
        data["next_action"],
        data.get("profession")
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))
    
    cursor.close()
    conn.close()

    return results

def get_followups_today():
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
        SELECT * FROM clients
        WHERE followup_date = %s
        AND status = 'Active'
        ORDER BY created_at DESC
    """, (today,))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

def get_client_by_id(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
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

def update_client(client_id, data):
    location_normalized = normalize_location(data.get("location"))
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clients
        SET name=%s,
            contact=%s,
            requirement=%s,
            property_type=%s,
            location=%s,
            location_normalized=%s,
            budget=%s,
            followup_date=%s,
            notes=%s,
            next_action=%s,                  
            profession=%s
        WHERE id=%s
    """, (
        data["name"],
        data["contact"],
        data["requirement"],
        data["property_type"],
        data["location"],
        data["budget"],
        data["followup_date"],
        data["notes"],
        data["next_action"],
        data.get("profession"),
        client_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

def get_matching_buyers_for_seller(seller):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Fetch all potential buyers (basic filter only)
    cursor.execute("""
        SELECT * FROM clients
        WHERE requirement = %s
        AND property_type = %s
        ORDER BY created_at DESC
    """, ("Buy", seller["property_type"]))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    buyers = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    # Step 2: Apply intelligent filtering in Python
    return filter_matching_buyers(seller, buyers)
