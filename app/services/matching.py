import re


def build_location_filter(client_location):
    """
    Returns:
        sql_condition (string)
        params (list)
    """

    if not client_location:
        return "", []

    # Split by common separators
    locations = re.split(r',|or|/|&|\|', client_location, flags=re.IGNORECASE)
    locations = [loc.strip() for loc in locations if loc.strip()]

    if not locations:
        return "", []

    sql = " AND ("
    params = []

    for i, loc in enumerate(locations):
        normalized = loc.lower().replace(" ", "").replace("-", "")

        sql += """
            REPLACE(REPLACE(LOWER(location), ' ', ''), '-', '')
            LIKE %s
        """
        params.append(f"%{normalized}%")

        if i < len(locations) - 1:
            sql += " OR"

    sql += ")"

    return sql, params