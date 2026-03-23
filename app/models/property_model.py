from app.db import get_db_connection
from app.services.matching import build_location_filter
from app.services.client_rules import map_client_requirement_to_property_mode
from app.services.query_builder import build_in_filter
from app.services.property_query import _build_property_query
from app.settings.constants import BUDGET_UPPER_MULTIPLIER, BUDGET_LOWER_MULTIPLIER
from app.logger import logger

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

def get_properties(
    search=None,
    mode_filters=None,
    active_filters=None,
    status_filters=None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query, params = _build_property_query(
        search,
        mode_filters,
        active_filters,
        status_filters
    )

    cursor.execute(query, tuple(params))

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

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
        SELECT * FROM broker_properties
        WHERE mode = %s
        AND type = %s
        AND is_available = TRUE
    """
    params = [mode, client["property_type"]]

    # Location matching — combine area_clusters AND location text with OR
    location_conditions = []
    location_params = []

    # area_clusters match
    if client.get("area_clusters"):
        placeholders = ",".join(["%s"] * len(client["area_clusters"]))
        location_conditions.append(f"area_cluster IN ({placeholders})")
        location_params.extend(client["area_clusters"])

    # location text match
    if client.get("location"):
        loc_sql, loc_params = build_location_filter(client.get("location"))
        if loc_sql:
            # strip the leading " AND (" and trailing ")" to embed in our OR block
            inner = loc_sql.strip().removeprefix("AND (").removesuffix(")")
            location_conditions.append(f"({inner})")
            location_params.extend(loc_params)
    
    if location_conditions:
        query += " AND (" + " OR ".join(location_conditions) + ")"
        params.extend(location_params)

    # Budget filter (±25%)
    if client["budget"]:
        lower = int(client["budget"] * BUDGET_LOWER_MULTIPLIER)
        upper = int(client["budget"] * BUDGET_UPPER_MULTIPLIER)
        query += " AND budget BETWEEN %s AND %s"
        params.extend([lower, upper])

    query += " ORDER BY created_at DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()
    logger.debug("FINAL QUERY: %s", query)
    logger.debug("PARAMS: %s", params)

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

def restore_property_by_id(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE properties
        SET is_active = TRUE
        WHERE id = %s
        AND is_active = FALSE
    """, (property_id,))

    conn.commit()
    cursor.close()
    conn.close()