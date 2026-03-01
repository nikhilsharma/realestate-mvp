from app.services.query_builder import build_in_filter

def _build_property_query(search, mode_filters, active_filters, status_filters):

    conditions = []
    params = []

    # is_active
    sql, p = build_in_filter("is_active", active_filters, convert_bool=True)
    if sql:
        conditions.append(sql.replace(" AND ", ""))
        params.extend(p)

    # status
    sql, p = build_in_filter("status", status_filters)
    if sql:
        conditions.append(sql.replace(" AND ", ""))
        params.extend(p)

    # mode
    sql, p = build_in_filter("mode", mode_filters)
    if sql:
        conditions.append(sql.replace(" AND ", ""))
        params.extend(p)

    # search
    if search:
        conditions.append("""
        (
            location ILIKE %s OR
            owner_name ILIKE %s OR
            dealer_name ILIKE %s
        )
        """)
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query = "SELECT * FROM properties"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    return query, params