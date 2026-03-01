def _build_client_query(search=None, lead_temperature=None, is_active=None):
    conditions = []
    params = []

    # ---------- Lead Temperature (OR inside group) ----------
    if lead_temperature:
        placeholders = ", ".join(["%s"] * len(lead_temperature))
        conditions.append(f"lead_temperature IN ({placeholders})")
        params.extend(lead_temperature)

    # ---------- Record State ----------
    if is_active:
        bool_values = [val == "true" for val in is_active]

        placeholders = ", ".join(["%s"] * len(bool_values))
        conditions.append(f"is_active IN ({placeholders})")
        params.extend(bool_values)

    # ---------- Search ----------
    if search:
        conditions.append("""
            (
                name ILIKE %s
                OR location ILIKE %s
                OR profession ILIKE %s
            )
        """)
        params.extend([
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ])
    # ---------- Final Query ----------
    query = "SELECT * FROM clients"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY lead_score DESC, created_at DESC"

    print("QUERY:", query)
    print("PARAMS:", params)

    return query, params