from app.models.broker_property_model import get_broker_properties_filtered, get_broker_property_count, get_matching_properties_count
from app.services.broker_visuals import decorate_broker_properties
import time
from app.logger import logger
from app.db import get_db_connection

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

def refresh_single_client_score(client, conn=None):
    own_connection = conn is None
    if own_connection:
        conn = get_db_connection()
    
    try:
        # Respect manual override
        if client.get("lead_temperature_override"):
            return

        # matching_count = len(get_matching_properties(client))
        matching_count = get_matching_properties_count(client, conn)
        score = calculate_lead_score(client, matching_count)
        temperature = classify_temperature(score)

        if (
            score != client.get("lead_score")
            or temperature != client.get("lead_temperature")
        ):
            update_lead_data(client["id"], score, temperature, conn)
        
        # print(f"***Client {client['id']}, {client['name']} → score: {score}, temp: {temperature}")
        # print(f"***Matching count: {matching_count}")
    
    finally:
        if own_connection:
            conn.commit()
            conn.close()

def refresh_lead_scores():
    conn = get_db_connection()

    clients = get_all_clients(conn)

    for client in clients:
        refresh_single_client_score(client, conn)

    conn.commit()
    conn.close()

def build_dashboard_context():
    start = time.time()
    # 1️⃣ Ensure scores are fresh
    refresh_lead_scores()
    elapsed = time.time() - start
    logger.info("refresh_lead_scores took %.3f seconds", elapsed)

    start = time.time()
    # 2️⃣ Fetch sections
    hot_leads = get_clients_by_temperature("hot")
    elapsed = time.time() - start
    followups = get_followups_today()
    logger.info("hot leads and follow up took %.3f seconds", elapsed)

    start = time.time()
    # Active properties (only need count)
    # data = get_broker_properties_filtered(
    # modes=["Sale", "Rent"],
    # is_available=["true"],
    # freshness=["fresh", "aging"],
    # page=1,
    # per_page=1   # minimal rows since we only need count
    # )
    
    # active_properties_count = data["total"]
    active_properties_count = get_broker_property_count(is_available=True)

    # Recent properties (display 5)
    data  = get_broker_properties_filtered(
    modes=["Sale", "Rent"],
    is_available=["true"],
    freshness=["fresh", "aging"],
    page=1,
    per_page=5
    )

    recent_properties = data["items"]

    # Archived properties (only need count)
    # data = get_broker_properties_filtered(
    # modes=["Sale", "Rent"],
    # is_available=["false"],
    # page=1,
    # per_page=1
    # )
    # archived_properties_count = data["total"]
    archived_properties_count = get_broker_property_count(is_available=False)


    elapsed = time.time() - start
    logger.info("Fetching active, archieved and recent properties took %.3f seconds", elapsed)

    # Only decorate the displayed items
    recent_properties = decorate_broker_properties(recent_properties)

    hot_leads_count = len(hot_leads)
    followups_count = len(followups)

    # 4️⃣ Structured stats (scalable)
    stats = [
        {
            "label": "Active Properties", 
            "value": active_properties_count,
            "url": "/broker-properties"
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
            "url": "/broker-properties?is_available=false"
        },
    ]

    return {
        "stats": stats,
        "hot_leads": hot_leads[:5],
        "followups": followups,
        "recent_properties": recent_properties
    }