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

def parse_client_form(form):
    followup_raw = form.get("followup_date")
    followup = followup_raw if followup_raw else None

    budget_raw = form.get("budget")
    budget = int(budget_raw) if budget_raw else None

    return {
        "name": form.get("name"),
        "contact": form.get("contact"),
        "requirement": form.get("requirement"),
        "property_type": form.get("property_type"),
        "location": form.get("location"),
        "budget": budget,
        "followup_date": followup,
        "notes": form.get("notes"),
        "next_action": form.get("next_action")
    }