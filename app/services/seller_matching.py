from app.services.location_utils import extract_keywords


def locations_match(seller_loc, buyer_loc):
    """
    Two-way keyword overlap matching.
    Ignores small words.
    """

    if not seller_loc or not buyer_loc:
        return False

    seller_keywords = extract_keywords(seller_loc)
    buyer_keywords = extract_keywords(buyer_loc)

    # Seller keyword inside buyer location
    for word in seller_keywords:
        if word in buyer_loc:
            return True

    # Buyer keyword inside seller location
    for word in buyer_keywords:
        if word in seller_loc:
            return True

    return False


def filter_matching_buyers(seller, buyers):
    """
    Python-side intelligent filtering.
    """

    matched = []

    seller_loc = seller.get("location_normalized")
    seller_budget = seller.get("budget")

    for buyer in buyers:

        buyer_loc = buyer.get("location_normalized")
        buyer_budget = buyer.get("budget")

        # --- Location check ---
        if not locations_match(seller_loc, buyer_loc):
            continue

        # --- Budget check (±10%) ---
        if seller_budget and buyer_budget:
            lower = int(seller_budget * 0.9)
            upper = int(seller_budget * 1.1)

            if not (lower <= buyer_budget <= upper):
                continue

        matched.append(buyer)

    return matched