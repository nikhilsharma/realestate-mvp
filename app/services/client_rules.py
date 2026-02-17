def map_client_requirement_to_property_mode(requirement):
    """
    Maps client requirement to property mode.
    Returns:
        property_mode (str) or None if no matching should occur
    """

    if requirement == "Rent":
        return "Rent"

    if requirement == "Buy":
        return "Sale"

    return None  # Sell clients do not need matches