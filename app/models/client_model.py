from app.db import get_db_connection
from datetime import date
from app.services.location_utils import normalize_location
from app.services.client_query_builder import _build_client_query
from app.services.seller_matching import filter_matching_buyers
from app.pagination import paginate_query
from app.logger import logger


def create_client(data):
    location_normalized = normalize_location(data.get("location"))
    conn = get_db_connection()
    cursor = conn.cursor()
    logger.debug("area_clusters>>>%s",data.get("area_clusters"))

    cursor.execute("""
        INSERT INTO clients
        (name, contact, requirement, property_type, area_clusters, location, 
                   location_normalized, budget, followup_date, status, notes, 
                   next_action, profession)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["name"],
        data["contact"],
        data["requirement"],
        data["property_type"],
        data.get("area_clusters"),
        data["location"],
        location_normalized,
        data["budget"],
        data["followup_date"],
        "Active",
        data["notes"],
        data["next_action"],
        data.get("profession")
    ))

    client_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return client_id


def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE is_active = TRUE ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    results = []
    for row in rows:
        results.append(dict(zip(columns, row)))
    
    cursor.close()
    conn.close()

    return results

def get_clients_filtered(
        search=None, 
        lead_temperature=None, 
        is_active=None, page=1,
        per_page=20,
        **_):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    base_query, params = _build_client_query(search=search, 
                                        lead_temperature=lead_temperature, 
                                        is_active=is_active)
    
    data = paginate_query(
        cursor,
        base_query,
        params,
        page,
        per_page
    )

    logger.debug("Base Query::: %s", base_query)
    logger.debug("Params::: %s", params)


    cursor.close()
    conn.close()

    return data

def get_followups_today():
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
        SELECT * FROM clients
        WHERE followup_date = %s
        AND status = 'Active'
        AND is_active = TRUE
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

    try:
        cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        row = cursor.fetchone()

        if not row:
            return None

        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    finally:
        cursor.close()
        conn.close()

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
            profession=%s,
            lead_temperature_override=%s,
            area_clusters = %s
        WHERE id=%s
    """, (
        data["name"],
        data["contact"],
        data["requirement"],
        data["property_type"],
        data["location"],
        location_normalized,
        data["budget"],
        data["followup_date"],
        data["notes"],
        data["next_action"],
        data.get("profession"),
        data.get("lead_temperature_override"),
        data.get("area_clusters"),
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
        AND is_active = TRUE
        ORDER BY created_at DESC
    """, ("Buy", seller["property_type"]))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    buyers = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    # Step 2: Apply intelligent filtering in Python
    return filter_matching_buyers(seller, buyers)

def soft_delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clients
        SET is_active = FALSE
        WHERE id = %s
    """, (client_id,))

    conn.commit()
    cursor.close()
    conn.close()

def update_lead_data(client_id, score, temperature):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clients
        SET lead_score = %s,
            lead_temperature = %s
        WHERE id = %s
    """, (score, temperature, client_id))

    conn.commit()
    cursor.close()
    conn.close()

def get_clients_by_temperature(temperature):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM clients
        WHERE COALESCE(lead_temperature_override, lead_temperature) = %s
        AND is_active = TRUE
        ORDER BY lead_score DESC, created_at DESC
    """, (temperature,))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return results