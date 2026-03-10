from app.models.broker_property_model import confirm_broker_property, toggle_broker_availability, create_broker_property

def confirm_broker_listing(property_id):
    confirm_broker_property(property_id)

def toggle_broker_listing(property_id):
    toggle_broker_availability(property_id)

def add_broker_property(data):
    return create_broker_property(data)
