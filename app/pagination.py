def paginate_query(cursor, base_query, params, page=1, per_page=20):
    """
    Executes paginated query and returns:
    results, total_count, total_pages
    """

    # Count total rows
    count_query = f"SELECT COUNT(*) FROM ({base_query}) AS subquery"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    # Pagination
    offset = (page - 1) * per_page
    paginated_query = base_query + " LIMIT %s OFFSET %s"
    paginated_params = list(params) + [per_page, offset]

    cursor.execute(paginated_query, paginated_params)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]

    total_pages = (total_count + per_page - 1) // per_page

    return {
        "items": results,
        "total": total_count,
        "pages": total_pages,
        "page": page
    }
