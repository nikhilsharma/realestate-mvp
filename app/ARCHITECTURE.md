ARCHITECTURE.md
1. System Philosophy
Urban Bricks & Bonds is designed as a server rendered Flask CRM optimized for:
• Speed of development
• Operational clarity for brokers
• Minimal infrastructure complexity
• Modular but simple architecture
Design principles:
• Thin routes
• Business logic in services
• SQL centralized in models/query builders
• Templates kept mostly logic free
• Mobile first UI
The system is intentionally monolithic but modular, allowing future evolution into a multi user SaaS without major rewrites.
________________________________________
2. High Level Architecture
Browser
   │
   ▼
Flask Routes
   │
   ▼
Service Layer
   │
   ▼
Model / Query Layer
   │
   ▼
PostgreSQL (Neon)
Templates render server side using Jinja2.
There is no heavy frontend framework.
________________________________________
3. Actual Project Structure
realestate-mvp/

app/
│
├── db.py
│
├── models/
│   ├── property_model.py
│   ├── client_model.py
│   └── broker_property_model.py
│
├── routes.py
│
├── services/
│   ├── dashboard_service.py
│   ├── clients_service.py
│   ├── broker_property_service.py
│   ├── matching.py
│   ├── seller_matching.py
│   ├── lead_scoring.py
│   ├── location_utils.py
│   ├── request_utils.py
│   ├── query_builder.py
│   ├── client_query_builder.py
│   ├── broker_query_builder.py
│   ├── property_query.py
│   ├── client_rules.py
│   └── broker_visuals.py
│
├── settings/
│   └── constants.py
│
├── tests/
│   └── test_matching.py
│
├── utils.py
│
└── __init__.py

app.py
run.py
config.py

/templates

________________________________________
4. Routing Layer
Routes are defined primarily in:
app/routes.py
Responsibilities:
• Receive HTTP requests
• Extract query parameters
• Call services
• Render templates
Routes intentionally contain minimal business logic.
Examples of routes implemented:
Route	Purpose
/	Dashboard
/properties	Property inventory
/broker-properties	Broker property leads
/add-property	Add property
/edit-property/<id>	Edit property
/clients	Client CRM
/add-client	Add client
/edit-client/<id>	Edit client
/buyer-matches/<id>	Matching buyers
/client-matches/<id>	Property matches
/login	Admin login
________________________________________
5. Database Layer
Database connection is handled via:
app/db.py
Uses:
psycopg
Database:
PostgreSQL (Neon)
Environment variable:
DATABASE_URL
________________________________________
6. Model Layer
Models are responsible only for executing SQL queries and returning rows.
Files:
property_model.py
client_model.py
broker_property_model.py
Responsibilities:
• Insert
• Update
• Fetch
• Soft delete (archive)
• Restore
Models do not implement business logic.
________________________________________
7. Service Layer
Services contain the real application logic.
Examples:
dashboard_service.py
Builds dashboard context including:
• Stats
• Hot leads
• Followups
• Recent properties
________________________________________
clients_service.py
Handles:
• Client filtering
• Client listing
• Followup logic
________________________________________
broker_property_service.py
Handles broker inventory workflow:
• Broker leads
• Visual cues
• Aging logic
________________________________________
matching.py
Responsible for:
Buyer ↔ Property matching
Uses:
• budget
• location
• property type
________________________________________
seller_matching.py
Matches sellers with buyers.
________________________________________
lead_scoring.py
Implements lead temperature classification:
Hot / Warm / Cold
Based on scoring constants.
________________________________________
request_utils.py
Extracts filters from request args.
Avoids repeating parsing logic across routes.
________________________________________
query_builder.py
Builds dynamic SQL filters like:
WHERE status IN (...)
Shared across modules.
________________________________________
8. Settings Layer
Constants are centralized in:
app/settings/constants.py
Examples:
• Hot lead thresholds
• Matching multipliers
This prevents magic numbers inside services.
________________________________________
9. Template Architecture
Templates live in:
templates/
Structure:
templates/

base.html

pages

add_property.html
edit_property.html
clients.html
dashboard.html

partials/
Partials provide reusable components such as:
• property cards
• status badges
• broker property visuals
Rules:
Full page → extends base.html
Partial → never extends base
________________________________________
10. Lead Intelligence
Lead intelligence currently includes:
• Lead temperature
• Followups
• Matching engine
Scoring logic:
lead_scoring.py
Matching logic:
matching.py
seller_matching.py
________________________________________
11. Broker Property System
Broker properties represent external listings or leads.
They support:
• Aging detection
• Visual highlighting
• Availability state
Logic implemented in:
broker_property_service.py
broker_visuals.py
________________________________________
12. Authentication
Currently minimal.
Login page:
/login
Future system will include:
• Multi user
• Broker accounts
• Role based access
________________________________________
13. Deployment
Hosting:
Render
Database:
Neon PostgreSQL
Environment:
.env
Important variables:
DATABASE_URL
SECRET_KEY
________________________________________
