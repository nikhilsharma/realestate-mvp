from app.services.request_utils import extract_client_filters
from app.models.client_model import get_clients_filtered, create_client, get_client_by_id, update_client
from app.services.dashboard_service import refresh_single_client_score
from app.models.broker_property_model import get_brokers_for_clients
from app.models.property_model import get_matching_properties
from app.services.broker_visuals import decorate_broker_properties
from app.models.broker_property_model import get_brokers_for_clients

def build_clients_context(request):
    filters = extract_client_filters(request)
    page = request.args.get("page", 1, type=int)
    data = get_clients_filtered(
        page=page,
        **filters
    )
    
    return {
        "clients": data["items"],
        "page": data["page"],
        "total_pages": data["pages"],
        **filters
    }

def create_client_service(data):
    client_id = create_client(data)
    client = get_client_by_id(client_id)
    refresh_single_client_score(client)
    return client_id

def update_client_service(client_id, data):
    update_client(client_id, data)
    client = get_client_by_id(client_id)
    refresh_single_client_score(client)

def enrich_clients_with_brokers(clients):
    # 1. Collect all area clusters
    all_areas = set()

    for client in clients:
        if client.get("area_clusters"):
            all_areas.update(client["area_clusters"])

    # 2. Fetch brokers in ONE query
    brokers_map = get_brokers_for_clients(list(all_areas))

    # 3. Attach to each client
    for client in clients:
        client["brokers"] = pick_top_brokers_per_client(client, brokers_map)
        
    return clients

def pick_top_brokers_per_client(client, brokers_map, limit=3):
    areas = client.get("area_clusters") or []

    selected = []
    used_phones = set()

    # 1. First pass → pick 1 broker per area
    for area in areas:
        brokers = brokers_map.get(area, [])
        for b in brokers:
            if b["phone"] not in used_phones:
                selected.append(b)
                used_phones.add(b["phone"])
                break  # only 1 per area

    # 2. Second pass → fill remaining slots
    if len(selected) < limit:
        for area in areas:
            brokers = brokers_map.get(area, [])
            for b in brokers:
                if b["phone"] not in used_phones:
                    selected.append(b)
                    used_phones.add(b["phone"])
                    if len(selected) >= limit:
                        break
            if len(selected) >= limit:
                break

    return selected

def get_client_matches_context(client):

    # 1. Properties
    properties = get_matching_properties(client)
    properties = decorate_broker_properties(properties)

    # 2. Brokers
    area_clusters = client.get("area_clusters") or []
    brokers = []

    if area_clusters:
        brokers_map = get_brokers_for_clients(area_clusters)

        brokers = pick_top_brokers_per_client(
            client,
            brokers_map,
            limit=5
        )

    return {
        "properties": properties,
        "brokers": brokers
    }