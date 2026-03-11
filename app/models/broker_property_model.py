from datetime import date
from app.db import get_db_connection
from app.services.broker_query_builder import _build_broker_query
from app.services.location_utils import normalize_location

def create_broker_property(data):
    location_normalized = normalize_location(data.get("location"))
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO broker_properties (
            area_cluster,
            configuration,
            location,
            location_normalized,
            budget,
            mode,
            type,
            video_link,
            broker_name,
            broker_contact,
            tags,
            last_confirmed_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["area_cluster"],
        data.get("configuration"),
        data["location"],
        location_normalized,
        data["budget"],
        data["mode"],
        data.get("type", "Residential"),
        data.get("video_link"),
        data.get("broker_name"),
        data.get("broker_contact"),
        data.get("tags", []),
        data["last_confirmed_at"]
    ))

    new_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return new_id


def get_broker_properties():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM broker_properties
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


def confirm_broker_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE broker_properties
        SET last_confirmed_at = %s
        WHERE id = %s
    """, (date.today(), property_id))

    conn.commit()
    cursor.close()
    conn.close()


def toggle_broker_availability(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE broker_properties
        SET is_available = NOT is_available
        WHERE id = %s
    """, (property_id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_broker_properties_filtered(
    area_clusters=None,
    configurations=None,
    modes=None,
    freshness=None,
    is_available=None,
    search=None,
    tags=None,
    **_
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query, params = _build_broker_query(
        area_clusters,
        configurations,
        modes,
        freshness,
        is_available,
        search,
        tags
    )
    print("QUERY:", query)
    print("PARAMS:", params)
    cursor.execute(query, params)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

def get_broker_property_by_id(property_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM broker_properties WHERE id = %s",
        (property_id,)
    )

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

def update_broker_property(property_id, data):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE broker_properties
    SET
        area_cluster=%s,
        configuration=%s,
        location=%s,
        budget=%s,
        mode=%s,
        type=%s,
        video_link=%s,
        broker_name=%s,
        broker_contact=%s,
        tags=%s,
        last_confirmed_at=%s
    WHERE id=%s
    """, (
        data["area_cluster"],
        data.get("configuration"),
        data["location"],
        data["budget"],
        data["mode"],
        data["type"],
        data["video_link"],
        data["broker_name"],
        data["broker_contact"],
        data["tags"],
        data["last_confirmed_at"],
        property_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

def update_whatsapp_ref(property_id, whatsapp_ref):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE broker_properties
        SET whatsapp_video_ref = %s
        WHERE id = %s
    """, (whatsapp_ref, property_id))

    conn.commit()
    cursor.close()
    conn.close()