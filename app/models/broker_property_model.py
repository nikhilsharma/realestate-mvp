from datetime import date
from app.db import get_db_connection
from app.services.broker_query_builder import _build_broker_query
from app.services.location_utils import normalize_location
from app.pagination import paginate_query
from app.logger import logger
from app.services.client_rules import map_client_requirement_to_property_mode
from app.settings.constants import BUDGET_UPPER_MULTIPLIER, BUDGET_LOWER_MULTIPLIER
from app.services.matching import build_location_filter


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
            area,
            mode,
            type,
            video_link,
            broker_name,
            broker_contact,
            owner_name,
            owner_contact,
            tags,
            last_confirmed_at,
            latitude,
            longitude,
            broker_chain_count    
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["area_cluster"],
        data.get("configuration"),
        data["location"],
        location_normalized,
        data["budget"],
        data.get("area"),
        data["mode"],
        data.get("type", "Residential"),
        data.get("video_link"),
        data.get("broker_name"),
        data.get("broker_contact"),
        data.get("owner_name"),
        data.get("owner_contact"),
        data.get("tags", []),
        data["last_confirmed_at"],
        data.get("latitude"),
        data.get("longitude"),
        data.get("broker_chain_count", 0)
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
    page=1,
    per_page=20,
    **_
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        base_query, params = _build_broker_query(
            area_clusters,
            configurations,
            modes,
            freshness,
            is_available,
            search,
            tags
        )
        logger.debug("QUERY: %s", base_query)
        logger.debug("PARAMS: %s", params)
        
        data = paginate_query(
            cursor,
            base_query,
            params,
            page,
            per_page
        )

        return data
    
    finally:
        cursor.close()
        conn.close()


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
        area=%s,
        mode=%s,
        type=%s,
        video_link=%s,
        broker_name=%s,
        broker_contact=%s,
        owner_name=%s,
        owner_contact=%s,
        tags=%s,
        last_confirmed_at=%s,
        latitude=%s,
        longitude=%s,
        broker_chain_count=%s
    WHERE id=%s
    """, (
        data["area_cluster"],
        data.get("configuration"),
        data["location"],
        data["budget"],
        data.get("area"),
        data["mode"],
        data["type"],
        data["video_link"],
        data["broker_name"],
        data["broker_contact"],
        data["owner_name"],
        data["owner_contact"],
        data["tags"],
        data["last_confirmed_at"],
        data.get("latitude"),
        data.get("longitude"),
        data.get("broker_chain_count", 0),
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

def get_broker_property_count(is_available=True):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM broker_properties 
            WHERE is_available = %s
        """, (is_available,))
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()

def get_matching_properties_count(client, conn=None):

    own_connection = conn is None
    if own_connection:
        conn = get_db_connection()
    
    cursor = conn.cursor()

    try:
        mode = map_client_requirement_to_property_mode(client.get("requirement"))

        if not mode:
            return 0

        query = """
            SELECT COUNT(*)
            FROM broker_properties
            WHERE is_available = TRUE
            AND mode = %s
            AND type = %s
        """
        params = [mode, client["property_type"]]

        # Location filters
        location_conditions = []
        location_params = []

        if client.get("area_clusters"):
            placeholders = ",".join(["%s"] * len(client["area_clusters"]))
            location_conditions.append(f"area_cluster IN ({placeholders})")
            location_params.extend(client["area_clusters"])

        if client.get("location"):
            loc_sql, loc_params = build_location_filter(client.get("location"))
            if loc_sql:
                inner = loc_sql.strip().removeprefix("AND (").removesuffix(")")
                location_conditions.append(f"({inner})")
                location_params.extend(loc_params)

        if location_conditions:
            query += " AND (" + " OR ".join(location_conditions) + ")"
            params.extend(location_params)

        # Budget
        if client.get("budget"):
            lower = int(client["budget"] * BUDGET_LOWER_MULTIPLIER)
            upper = int(client["budget"] * BUDGET_UPPER_MULTIPLIER)
            query += " AND budget BETWEEN %s AND %s"
            params.extend([lower, upper])

        cursor.execute(query, tuple(params))
        return cursor.fetchone()[0]

    finally:
        cursor.close()
        if own_connection:
            conn.close()

def get_brokers_for_clients(area_clusters_list):
    """
    area_clusters_list: list of all unique area clusters across all clients on the page
    Returns: dict of {area_cluster: [brokers]}
    """
    if not area_clusters_list:
        return {}

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            broker_name,
            broker_contact,
            area_cluster,
            COUNT(*) as listings
        FROM broker_properties
        WHERE broker_name IS NOT NULL
        AND broker_contact IS NOT NULL
        AND area_cluster = ANY(%s)
        GROUP BY broker_name, broker_contact, area_cluster
        ORDER BY listings DESC
    """, (area_clusters_list,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group by area_cluster
    result = {}
    for row in rows:
        broker_name, broker_contact, area_cluster, listings = row
        if area_cluster not in result:
            result[area_cluster] = []
        result[area_cluster].append({
            "name": broker_name,
            "phone": broker_contact,
            "area": area_cluster,
            "listings": listings
        })

    return result