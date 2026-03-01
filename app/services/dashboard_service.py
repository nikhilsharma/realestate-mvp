from app.models.client_model import (
    get_all_clients,
    update_lead_data,
    get_clients_by_temperature,
    get_followups_today
)

from app.models.property_model import get_matching_properties, get_properties

from app.services.lead_scoring import (
    calculate_lead_score,
    classify_temperature
)

def refresh_lead_scores():
    clients = get_all_clients()

    for client in clients:
        matching_count = len(get_matching_properties(client))
        score = calculate_lead_score(client, matching_count)
        temperature = classify_temperature(score)

        if (
            score != client.get("lead_score")
            or temperature != client.get("lead_temperature")
        ):
            update_lead_data(client["id"], score, temperature)


def build_dashboard_context():
    # 1️⃣ Ensure scores are fresh
    refresh_lead_scores()

    # 2️⃣ Fetch sections
    hot_leads = get_clients_by_temperature("hot")
    followups = get_followups_today()

    active_properties = get_properties(
        search="",
        mode_filters=["Sale", "Rent"],
        active_filters=["true"],
        status_filters=["Available"]
    )

    recent_properties = get_properties(
    search="",
    mode_filters=["Sale", "Rent"],
    active_filters=["true"],
    status_filters=["Available"]
    )[:5]

    archived_properties = get_properties(
        search="",
        mode_filters=["Sale", "Rent"],
        active_filters=["false"],
        status_filters=["Available", "Closed"]
    )

    active_properties_count = len(active_properties)
    archived_properties_count = len(archived_properties)
    hot_leads_count = len(hot_leads)
    followups_count = len(followups)

    # 4️⃣ Structured stats (scalable)
    stats = [
        {
            "label": "Active Properties", 
            "value": active_properties_count,
            "url": "/properties?is_active=true&status=Available"
        },
        {
            "label": "Hot Leads", 
            "value": hot_leads_count,
            "url": "/clients?lead_temperature=hot"    
        },
        {
            "label": "Followups Today", 
            "value": followups_count,
            "url": "/clients/followups"    
        },
        {
            "label": "Archived Properties", 
            "value": archived_properties_count,
            "url": "/properties?is_active=false"
        },
    ]

    return {
        "stats": stats,
        "hot_leads": hot_leads[:5],
        "followups": followups,
        "recent_properties": recent_properties
    }