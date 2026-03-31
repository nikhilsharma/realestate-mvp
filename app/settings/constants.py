# Lead scoring thresholds
HOT_LEAD_THRESHOLD = 60
WARM_LEAD_THRESHOLD = 30

# Budget tolerance multiplier +-25%
BUDGET_LOWER_MULTIPLIER = 0.75
BUDGET_UPPER_MULTIPLIER = 1.25

# Broker Inventory Freshness Rules

FRESH_DAYS_THRESHOLD = 3
AGING_DAYS_THRESHOLD = 7

DEFAULT_BROKER_FRESHNESS = ["fresh", "aging"]
DEFAULT_BROKER_AVAILABILITY = ["true"]

# Broker Property Tags
BROKER_PROPERTY_TAGS = [
    "Corner",
    "Park Facing",
    "Lift",
    "Parking",
    "Ground Floor",
    "First Floor",
    "Second Floor",
    "Third Floor",
    "DDA Flats",
    "Builder Floor",
    "Independent Floor",
    "New Construction",
    "Semi Furnished",
    "Fully Furnished",
    "Gated Society",
    "Ready to Move"
]

# Area Clusters
AREA_CLUSTERS = [
    "Janakpuri",
    "Tilak Nagar",
    "Mahavir Nagar",
    "Uttam Nagar",
    "Dwarka",
    "Vikaspuri",
    "Hari Nagar",
    "Subhash Nagar"
]

AREA_CODES = {
    "Janakpuri": "JP",
    "Tilak Nagar": "TN",
    "Mahavir Nagar": "MN",
    "Uttam Nagar": "UN",
    "Dwarka": "DW",
    "Vikaspuri": "VP",
    "Hari Nagar": "HN",
    "Subhash Nagar": "SN"
}

PROPERTY_MODE_CODES = {
    "Rent": "R",
    "Sale": "S"
}

# Property Configurations
CONFIGURATIONS = [
    "1RK",
    "1+1",
    "1BHK",
    "2BHK",
    "3BHK",
    "4BHK",
    "Builder Floor",
    "Shop",
    "Office",
    "Plot",
    "PG",
    "Upper Ground"
]

# How broker_properties are sorted:
# Direct Deals First
# Then last_confirmed_at
# Finally with created_at
BROKER_PROPERTY_ORDER_BY = " ORDER BY COALESCE(broker_chain_count, 1) ASC, last_confirmed_at DESC NULLS LAST, created_at DESC"