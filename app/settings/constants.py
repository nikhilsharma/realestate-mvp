# Lead scoring thresholds
HOT_LEAD_THRESHOLD = 60
WARM_LEAD_THRESHOLD = 30

# Budget tolerance multiplier
BUDGET_LOWER_MULTIPLIER = 0.85
BUDGET_UPPER_MULTIPLIER = 1.15

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
    "1BHK",
    "2BHK",
    "3BHK",
    "4BHK",
    "Builder Floor",
    "Shop",
    "Office"
]