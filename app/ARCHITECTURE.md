# 📄 ARCHITECTURE.md

Create:

```
ARCHITECTURE.md
```

Paste:

---

# 🏗 Urban Bricks & Bonds – Architecture Document

---

## 1️⃣ System Overview

Urban Bricks & Bonds is a lightweight CRM designed for small real estate brokers operating in Delhi NCR.

It manages:

* Property Inventory
* Clients (Buyers / Sellers / Renters)
* Matching logic
* Lifecycle (Available / Sold / Archived)
* WhatsApp property sharing

---

## 2️⃣ Technology Stack

| Layer    | Technology         |
| -------- | ------------------ |
| Backend  | Flask              |
| Database | PostgreSQL (Neon)  |
| Hosting  | Render             |
| Frontend | Bootstrap 5        |
| Language | Python 3           |
| ORM      | Raw SQL (psycopg2) |

---

## 3️⃣ High-Level Architecture

```
Browser
   ↓
Flask Routes
   ↓
Service Layer (Business Logic)
   ↓
Model Layer (SQL + DB Access)
   ↓
PostgreSQL (Neon)
```

---

## 4️⃣ Application Structure

```
app/
│
├── __init__.py
├── db.py
├── routes.py
│
├── models/
│    ├── property_model.py
│    └── client_model.py
│
├── services/
│    ├── matching.py
│    ├── seller_matching.py
│    ├── location_utils.py
│    ├── query_builder.py
│    └── request_utils.py
│
├── templates/
│    ├── dashboard.html
│    ├── clients.html
│    └── partials/
│         ├── property_card.html
│         ├── property_status_badge.html
│         ├── property_actions.html
│         └── property_share_button.html
│
└── static/
     ├── css/
     └── js/
```

---

## 5️⃣ Layer Responsibilities

### Routes Layer

* Handles HTTP
* Extracts request data
* Calls model/service functions
* Renders templates
* Should remain thin

---

### Model Layer

* Executes SQL
* Maps rows to dictionaries
* Contains no business logic

---

### Service Layer

Contains business rules such as:

* Location normalization
* Buyer/Seller matching
* Filter query building
* Request parsing

This layer isolates complexity.

---

## 6️⃣ Database Design

### Properties Table

| Column              | Purpose                  |
| ------------------- | ------------------------ |
| id                  | Primary key              |
| type                | Residential / Commercial |
| mode                | Rent / Sale              |
| location            | Raw location             |
| location_normalized | Matching logic           |
| budget              | Integer                  |
| area                | Sq ft                    |
| owner_name          | Optional                 |
| owner_contact       | Optional                 |
| dealer_name         | Optional                 |
| dealer_contact      | Optional                 |
| video_link          | Optional                 |
| status              | Available / Closed       |
| is_active           | Soft delete              |
| created_at          | Timestamp                |

---

### Clients Table

| Column              | Purpose                  |
| ------------------- | ------------------------ |
| id                  | Primary key              |
| name                | Client name              |
| contact             | Phone                    |
| requirement         | Rent / Buy / Sell        |
| property_type       | Residential / Commercial |
| location            | Raw                      |
| location_normalized | Matching                 |
| budget              | Integer                  |
| followup_date       | Date                     |
| status              | Active                   |
| notes               | Free text                |
| next_action         | Short instruction        |
| profession          | Useful for rentals       |
| is_active           | Soft delete              |
| created_at          | Timestamp                |

---

## 7️⃣ Lifecycle Model

Property:

```
Available → Sold → Archived → Restore
```

Client:

```
Active → Archived → Restore
```

Archived ≠ Sold
Archived = Soft deleted record

---

## 8️⃣ Matching Strategy

Buyer → Properties:

* Mode match
* Type match
* Budget ±10%
* Location normalized matching

Seller → Buyers:

* Reverse match
* Filtering done partially in Python

---

## 9️⃣ Security

* Session-based login
* Environment variables for secrets
* Database URL via Render secrets
* No hardcoded credentials

---

## 🔟 Scalability Notes

Current design supports:

* ~500 properties comfortably
* ~1000 clients comfortably

Future scaling improvements:

* Pagination
* Index on location_normalized
* Multi-user system
* Role-based access
* Tenant separation (multi-broker SaaS)

---

# 📌 Architecture Status

Current system is:

* Modular
* Maintainable
* Extensible
* Suitable for single broker usage
* Ready for SaaS evolution

---
