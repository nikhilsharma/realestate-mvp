from app.services.request_utils import extract_client_filters
from app.models.client_model import get_clients_filtered, create_client, get_client_by_id
from app.services.dashboard_service import refresh_single_client_score


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
