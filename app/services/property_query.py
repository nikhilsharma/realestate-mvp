from app.services.query_builder import build_in_filter

def _build_property_query(search, mode, active_filters, status_filters):

    # Defaults
    active_filters = active_filters or ["true"]
    status_filters = status_filters or ["Available"]

    conditions = []
    params = []

    # is_active filter
    sql, p = build_in_filter("is_active", active_filters, convert_bool=True)
    if sql:
        conditions.append(sql.replace(" AND ", ""))
        params.extend(p)

    # status filter
    sql, p = build_in_filter("status", status_filters)
    if sql:
        conditions.append(sql.replace(" AND ", ""))
        params.extend(p)

    # search filter
    if search and search.strip():
        conditions.append("(location ILIKE %s OR owner_name ILIKE %s)")
        params.extend([f"%{search.strip()}%", f"%{search.strip()}%"])

    # mode filter
    if mode and mode.strip():
        conditions.append("mode = %s")
        params.append(mode.strip())

    # Final query assembly
    query = "SELECT * FROM properties"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    return query, params