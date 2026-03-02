# Urban Bricks & Bonds – Architecture Overview

## 1. System Philosophy

This application follows a:

- Server-rendered Flask architecture
- Modular template composition
- Clear separation of:
  - Full pages
  - Reusable partials
  - Business logic
  - Query builders
  - Services

Mobile-first UI design.

---

## 2. Routing Structure

### Core Routes

| Route | Purpose |
|--------|----------|
| `/` | Dashboard (Operational overview) |
| `/properties` | Property Inventory Page |
| `/property/<id>` | Property Detail View |
| `/edit-property/<id>` | Edit Property |
| `/clients` | Clients Page (Filter-driven) |
| `/clients/followups` | Followups Today Workflow |

---

## 3. Layered Architecture

### Routes Layer
- Minimal logic
- Delegates to services
- Passes context to templates

### Service Layer
- `dashboard_service.py`
- `request_utils.py`
- `matching.py`
- `query_builder.py`

Handles:
- Context building
- Filter extraction
- Scoring refresh
- Query assembly

### Model Layer
- `property_model.py`
- `client_model.py`

Responsible only for:
- DB queries
- Data formatting

---

## 4. Template Structure
# Urban Bricks & Bonds – Architecture Overview

## 1. System Philosophy

This application follows a:

- Server-rendered Flask architecture
- Modular template composition
- Clear separation of:
  - Full pages
  - Reusable partials
  - Business logic
  - Query builders
  - Services

Mobile-first UI design.

---

## 2. Routing Structure

### Core Routes

| Route | Purpose |
|--------|----------|
| `/` | Dashboard (Operational overview) |
| `/properties` | Property Inventory Page |
| `/property/<id>` | Property Detail View |
| `/edit-property/<id>` | Edit Property |
| `/clients` | Clients Page (Filter-driven) |
| `/clients/followups` | Followups Today Workflow |

---

## 3. Layered Architecture

### Routes Layer
- Minimal logic
- Delegates to services
- Passes context to templates

### Service Layer
- `dashboard_service.py`
- `request_utils.py`
- `matching.py`
- `query_builder.py`

Handles:
- Context building
- Filter extraction
- Scoring refresh
- Query assembly

### Model Layer
- `property_model.py`
- `client_model.py`

Responsible only for:
- DB queries
- Data formatting

---

## 4. Template Structure
templates/
│
├── base.html
├── dashboard.html
├── properties.html
├── property_detail.html
├── edit_property.html
├── clients.html
│
└── partials/
├── dashboard/
├── properties/
├── clients/


### Rule

- Full page → extends `base.html`
- Partial → never extends base
- Components reused wherever possible

---

## 5. Filtering System Design

### Properties

Supports multi-select filtering for:
- Mode (Rent, Sale)
- Status (Available, Closed)
- Record state (Active, Archived)
- Search (location + owner)

Query builder uses:
- `build_in_filter()`
- Dynamic WHERE clause assembly

---

### Clients

Supports multi-select filtering for:
- Lead temperature (Hot, Warm, Cold)
- Record state (Active, Archived)
- Search (name + location + profession)

Followups is a dedicated workflow route, not just a filter.

---

## 6. Lead Intelligence

Lead scoring is controlled by constants:

- HOT_LEAD_THRESHOLD
- WARM_LEAD_THRESHOLD
- Budget matching multipliers

Matching logic lives in:
`matching.py`

No hardcoded values inside query layer.

---

## 7. UI Architecture

Dashboard is split into:

- Stats Zone
- Priority Zone (Hot Leads + Followups)
- Recent Properties
- Quick Navigation

Properties and Clients use consistent:

- Control Zone (Filters + Search)
- Inventory Zone (Cards Grid)

---

## 8. Reusability Principles

- `property_status_badge` reused everywhere
- `property_actions` reused on cards & detail page
- Shared filter CSS
- Shared spinner behavior

No duplication of business logic in templates.

---

## 9. Future Scalability

System is structured to support:

- Pagination
- Image uploads
- Client detail pages
- Match count badges
- Overdue followups
- Analytics dashboard