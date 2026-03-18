from app.services.request_utils import extract_client_filters
from app.models.client_model import get_clients_filtered


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