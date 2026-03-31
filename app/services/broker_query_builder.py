from app.settings.constants import (
    FRESH_DAYS_THRESHOLD,
    AGING_DAYS_THRESHOLD,
    BROKER_PROPERTY_ORDER_BY
)
from app.services.location_utils import normalize_location

def _build_broker_query(
    area_clusters,
    configurations,
    modes,
    freshness,
    is_available,
    search,
    tags
):
    conditions = []
    params = []

    # -------- Configuration --------
    if configurations:
        placeholders = ", ".join(["%s"] * len(configurations))
        conditions.append(f"configuration IN ({placeholders})")
        params.extend(configurations)

    # -------- Tags --------
    if tags:
        conditions.append(
            "EXISTS (SELECT 1 FROM unnest(tags) t WHERE t = ANY(%s))"
        )
        params.append(tags)

    # -------- Area Cluster --------
    if area_clusters:
        placeholders = ", ".join(["%s"] * len(area_clusters))
        conditions.append(f"area_cluster IN ({placeholders})")
        params.extend(area_clusters)

    # -------- Mode --------
    if modes:
        placeholders = ", ".join(["%s"] * len(modes))
        conditions.append(f"mode IN ({placeholders})")
        params.extend(modes)

    # -------- Availability --------
    if is_available:
        bool_values = []
        for val in is_available:
            if val == "true":
                bool_values.append(True)
            elif val == "false":
                bool_values.append(False)

        if bool_values:
            placeholders = ", ".join(["%s"] * len(bool_values))
            conditions.append(f"is_available IN ({placeholders})")
            params.extend(bool_values)

    # -------- Freshness --------
    freshness_conditions = []

    if freshness:
        for f in freshness:

            if f == "fresh":
                freshness_conditions.append(
                    f"(last_confirmed_at IS NOT NULL AND "
                    f"(CURRENT_DATE - last_confirmed_at <= {FRESH_DAYS_THRESHOLD}))"
                )

            elif f == "aging":
                freshness_conditions.append(
                    f"(last_confirmed_at IS NOT NULL AND "
                    f"(CURRENT_DATE - last_confirmed_at > {FRESH_DAYS_THRESHOLD} "
                    f"AND CURRENT_DATE - last_confirmed_at <= {AGING_DAYS_THRESHOLD}))"
                )

            elif f == "stale":
                freshness_conditions.append(
                    f"(last_confirmed_at IS NOT NULL AND "
                    f"(CURRENT_DATE - last_confirmed_at > {AGING_DAYS_THRESHOLD}))"
                )

        if freshness_conditions:
            conditions.append("(" + " OR ".join(freshness_conditions) + ")")

    # -------- Search --------
    if search:
        normalized = normalize_location(search)
        conditions.append("location_normalized ILIKE %s")
        params.append(f"%{normalized}%")

    # -------- Final Query --------
    query = "SELECT * FROM broker_properties"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += BROKER_PROPERTY_ORDER_BY

    return query, params