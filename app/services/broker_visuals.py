from datetime import date
from app.settings.constants import FRESH_DAYS_THRESHOLD, AGING_DAYS_THRESHOLD


def decorate_broker_properties(properties):

    today = date.today()

    for p in properties:

        p["freshness"] = "unknown"
        p["freshness_border"] = ""

        if not p.get("last_confirmed_at"):
            continue

        days = (today - p["last_confirmed_at"]).days
        p["days_since_confirm"] = days

        if days <= FRESH_DAYS_THRESHOLD:
            p["freshness"] = "fresh"
            p["freshness_border"] = "border-success"

        elif days <= AGING_DAYS_THRESHOLD:
            p["freshness"] = "aging"
            p["freshness_border"] = "border-warning"

        else:
            p["freshness"] = "stale"
            p["freshness_border"] = "border-danger"

        # Broker Chain
        chain = p.get("broker_chain_count", 0)

        if chain == 0:
            p["chain_label"] = "Direct ⭐"
            p["chain_color"] = "success"
        elif chain == 1:
            p["chain_label"] = "1 Broker"
            p["chain_color"] = "warning"
        elif chain == 2:
            p["chain_label"] = "2 Brokers"
            p["chain_color"] = "warning"
        else:
            p["chain_label"] = "3+ Brokers"
            p["chain_color"] = "danger"

    return properties