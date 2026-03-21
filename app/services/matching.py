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
    locations = re.split(r',|\band\b|\bor\b|/|&|\|', client_location, flags=re.IGNORECASE)
    locations = [loc.strip() for loc in locations if loc.strip()]

    if not locations:
        return "", []

    sql = " AND ("
    params = []

    for i, loc in enumerate(locations):
        normalized = loc.lower().replace(" ", "").replace("-", "")

        sql += """
            location_normalized LIKE %s
            OR REPLACE(REPLACE(LOWER(area_cluster), ' ', ''), '-', '') LIKE %s
            OR %s LIKE CONCAT('%%', REPLACE(REPLACE(LOWER(area_cluster), ' ', ''), '-', ''), '%%')
        """
        params.append(f"%{normalized}%")
        params.append(f"%{normalized}%")
        params.append(normalized)          # area_cluster in client location

        if i < len(locations) - 1:
            sql += " OR"

    sql += ")"

    return sql, params