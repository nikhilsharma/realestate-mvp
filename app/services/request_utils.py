def extract_filters(request):
    return {
        "active_filters": request.args.getlist("is_active") or ["true"],
        "status_filters": request.args.getlist("status") or ["Available"],
        "mode": request.args.get("mode"),
        "search": request.args.get("search")
    }

def extract_property_filters(request):
    return {
        "active_filters": request.args.getlist("is_active") or ["true"],
        "status_filters": request.args.getlist("status") or ["Available"],
        "mode_filters": request.args.getlist("mode") or ["Sale", "Rent"],
        "search": (request.args.get("search") or "").strip()
    }

def extract_client_filters(request):
    lead_temperature = request.args.getlist("lead_temperature")
    is_active = apply_default_record_filter(request.args.getlist("is_active"))
    search = request.args.get("search")

    return {
        "lead_temperature": lead_temperature,
        "is_active": is_active,
        "search": search
    }

def apply_default_record_filter(is_active):
    return is_active or ["true"]