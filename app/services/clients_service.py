from app.services.request_utils import extract_client_filters
from app.models.client_model import get_clients_filtered


def build_clients_context(request):
    filters = extract_client_filters(request)
    clients = get_clients_filtered(**filters)

    return {
        "clients": clients,
        **filters
    }