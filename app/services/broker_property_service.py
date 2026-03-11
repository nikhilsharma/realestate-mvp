from app.models.broker_property_model import confirm_broker_property, toggle_broker_availability, create_broker_property, update_whatsapp_ref
from app.settings.constants import AREA_CODES

def confirm_broker_listing(property_id):
    confirm_broker_property(property_id)

def toggle_broker_listing(property_id):
    toggle_broker_availability(property_id)

def add_broker_property(data):
    new_id = create_broker_property(data)
    whatsapp_ref = _generate_whatsApp_code(data, new_id)
    update_whatsapp_ref(property_id = new_id, whatsapp_ref = whatsapp_ref)
    return new_id

def _generate_whatsApp_code(data, new_id):
    area_code = AREA_CODES.get(data["area_cluster"], "XX")
    config = data.get("configuration", "NA")
    property_id_str = str(new_id).zfill(3)
    rent_sale = data.get("mode","X")
    whatsapp_ref = f"UBB-BRK-{property_id_str}-{area_code}-{config}-{rent_sale}"
    return whatsapp_ref
