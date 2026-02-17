def normalize_location(value):
    if not value:
        return None
    return value.lower().replace(" ", "").replace("-", "")


def extract_keywords(location):
    """
    Break location into meaningful keywords.
    Ignores very small words (<=3 characters).
    """
    if not location:
        return []

    words = location.lower().replace("-", " ").split()
    return [w for w in words if len(w) > 3]