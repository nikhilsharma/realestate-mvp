def parse_property_form(form):
    return {
        "type": form.get("type"),
        "mode": form.get("mode"),
        "location": form.get("location"),
        "budget": int(form.get("budget", 0)),
        "area": int(form.get("area", 0)),
        "owner_name": form.get("owner_name"),
        "owner_contact": form.get("owner_contact")
    }