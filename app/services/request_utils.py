def extract_filters(request):
    return {
        "active_filters": request.args.getlist("is_active") or ["true"],
        "status_filters": request.args.getlist("status") or ["Available"],
        "mode": request.args.get("mode"),
        "search": request.args.get("search")
    }