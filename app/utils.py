from datetime import datetime, date
from urllib.parse import urlencode, urlparse, parse_qs
from app.logger import logger
from app.services.validation import ValidationError

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

    requirement = form.get("requirement")

    area_clusters = form.getlist("area_clusters[]") or None
    logger.debug("Form.getlist area_clusters %s", form.getlist("area_clusters[]"))
    if requirement == "Sell" and area_clusters:
        area_clusters = [area_clusters[0]]  # ← enforce single for Sell
    
    if not area_clusters:
        raise ValidationError("area_clusters", "Please select at least one area cluster")

    return {
        "name": form.get("name"),
        "contact": form.get("contact"),
        "requirement": requirement,
        "property_type": form.get("property_type"),
        "location": form.get("location"),
        "budget": budget,
        "followup_date": followup,
        "notes": form.get("notes"),
        "next_action": form.get("next_action"),
        "profession": form.get("profession"),
        "lead_temperature_override": form.get("lead_temperature_override") or None,
        "area_clusters": area_clusters
    }

def parse_broker_property_form(form):

    tags = form.getlist("tags") or []

    last_confirmed_raw = form.get("last_confirmed_at")

    if last_confirmed_raw:
        last_confirmed_at = datetime.strptime(last_confirmed_raw, "%Y-%m-%d").date()
    else:
        last_confirmed_at = date.today()

    chain_raw = form.get("broker_chain_count")
    broker_chain_count = int(chain_raw) if chain_raw else 0

    area_clusters = form.getlist("area_cluster[]")
    area_cluster = area_clusters[0] if area_clusters else None

    if not area_cluster:
        raise ValidationError("area_cluster", "Please select an area cluster")

    logger.debug("Form.getlist area_clusters %s", form.getlist("area_clusters[]"))

    return {
        "area_cluster": area_cluster,
        "configuration": form.get("configuration"),
        "location": form.get("location"),
        "budget": int(form.get("budget", "0").replace(",", "")),
        "area": int(form["area"]) if form.get("area") else None,
        "mode": form.get("mode"),
        "type": form.get("type"),
        "video_link": form.get("video_link") or None,
        "broker_name": form.get("broker_name") or None,
        "broker_contact": form.get("broker_contact") or None,
        "owner_name": form.get("owner_name") or None,
        "owner_contact": form.get("owner_contact") or None,
        "tags": tags,
        "last_confirmed_at": last_confirmed_at,
        "latitude": float(form.get("latitude")) if form.get("latitude") else None,
        "longitude": float(form.get("longitude")) if form.get("longitude") else None,
        "broker_chain_count": broker_chain_count
    }

def build_next_page_url(request, next_page, filters=None):
    logger.debug("In build next page url method")
    params = request.args.to_dict(flat=False)  # preserves lists

    # if defaults were applied in Python but not in URL, add them explicitly
    if filters:
        for key, value in filters.items():
            if key not in params and value:
                params[key] = value if isinstance(value, list) else [value]

    logger.debug("PARAMS>> %s ", params)
    params["page"] = next_page       # just bump the page
    return f"{request.path}?{urlencode(params, doseq=True)}"

def format_inr(value):
    if value is None:
        return "N/A"
    try:
        value = int(value)
        s = str(value)
        if len(s) <= 3:
            return f"₹ {s}"
        # Indian format: last 3 digits, then groups of 2
        last3 = s[-3:]
        rest = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        return "₹ " + ",".join(groups) + "," + last3
    except:
        return f"₹ {value}"