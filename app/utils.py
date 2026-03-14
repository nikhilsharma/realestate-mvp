from datetime import datetime, date

def parse_property_form(form):
    return {
        "type": form.get("type"),
        "mode": form.get("mode"),
        "location": form.get("location"),
        "budget": int(form.get("budget", "0").replace(",", "")),
        "area": int(form.get("area", 0)),
        "owner_name": form.get("owner_name"),
        "owner_contact": form.get("owner_contact"),
        "video_link": form.get("video_link") or None,
        "dealer_name": form.get("dealer_name") or None,
        "dealer_contact": form.get("dealer_contact") or None
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
        "next_action": form.get("next_action"),
        "profession": form.get("profession"),
        "lead_temperature_override": form.get("lead_temperature_override")
    }

def parse_broker_property_form(form):

    tags = form.getlist("tags") or []

    last_confirmed_raw = form.get("last_confirmed_at")

    if last_confirmed_raw:
        last_confirmed_at = datetime.strptime(last_confirmed_raw, "%Y-%m-%d").date()
    else:
        last_confirmed_at = date.today()

    return {
        "area_cluster": form.get("area_cluster"),
        "configuration": form.get("configuration"),
        "location": form.get("location"),
        "budget": int(form.get("budget", "0").replace(",", "")),
        "mode": form.get("mode"),
        "type": form.get("type"),
        "video_link": form.get("video_link") or None,
        "broker_name": form.get("broker_name") or None,
        "broker_contact": form.get("broker_contact") or None,
        "owner_name": form.get("owner_name") or None,
        "owner_contact": form.get("owner_contact") or None,
        "tags": tags,
        "last_confirmed_at": last_confirmed_at
    }