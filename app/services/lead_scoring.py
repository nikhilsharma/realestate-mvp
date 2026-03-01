from datetime import date
from app.config.constants import HOT_LEAD_THRESHOLD
from app.config.constants import WARM_LEAD_THRESHOLD

def calculate_lead_score(client, matching_properties_count):
    score = 0

    # 1. Follow-up urgency
    if client.get("followup_date"):
        if client["followup_date"] <= date.today():
            score += 30

    # 2. Inventory match strength
    if matching_properties_count >= 3:
        score += 25
    elif matching_properties_count >= 1:
        score += 10

    # 3. Buying intent signal
    if client.get("next_action"):
        if "visit" in client["next_action"].lower():
            score += 20

    # 4. Fresh lead bonus
    if client.get("created_at"):
        days_old = (date.today() - client["created_at"].date()).days
        if days_old <= 7:
            score += 10

    return score

def classify_temperature(score):
    if score >= HOT_LEAD_THRESHOLD: # Temp Test
        return "hot"
    elif score >= WARM_LEAD_THRESHOLD:
        return "warm"
    return "cold"

def enrich_client_with_lead_data(client, matching_properties_count):
    score = calculate_lead_score(client, matching_properties_count)
    temperature = classify_temperature(score)

    client["lead_score"] = score
    client["lead_temperature"] = temperature

    return client