def build_in_filter(column_name, values, convert_bool=False):
    """
    Returns SQL clause + params for IN filtering.
    """
    if not values:
        return "", []

    params = []
    placeholders = []

    for v in values:
        if convert_bool:
            params.append(v.lower() == "true")
        else:
            params.append(v)
        placeholders.append("%s")

    sql = f" AND {column_name} IN ({', '.join(placeholders)})"
    return sql, params