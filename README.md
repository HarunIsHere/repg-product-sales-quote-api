# RePG Product, Sales & Quote Management API

Backend API for managing products, quotes, and orders for RePG’s B2B operations.

---

## 🚀 Live API

Swagger Docs:  
https://repg-product-sales-quote-api.onrender.com/docs

---

## API Overview

- /auth
- /users
- /products
- /quotes
- /orders

---

## ⚙️ Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- JWT Authentication (python-jose)
- Pydantic
- Uvicorn
- Render

---

## 📦 Features

- User authentication (JWT)
- Role-based access:
  - User
  - Admin
  - Super Admin
- Product management
- Quote creation and tracking
- Quote approval workflow
- Order creation from approved quotes
- Order item snapshot logic
- Status workflow (quotes → orders)
- Pagination for products, quotes, and orders
- Admin listing endpoints for quotes, orders, and users

---

## 🔐 Initial Access

Super Admin credentials:

```json
{
  "email": "admin@repg.com.tr",
  "password": "ChangeThisNow123!"
}
```

---

## 🧪 API Testing (Swagger)

1. Open:  
   https://repg-product-sales-quote-api.onrender.com/docs

2. Login:
   - POST /auth/login

3. Copy `access_token`

4. Click **Authorize** and paste token

---

## 🔄 Main Workflow

### 1. User Flow
- Register → `/users/`
- Login → `/auth/login`
- Browse products → `/products/`
- Create quote → `/quotes/`
- View own quotes → `/quotes/my`
- View own orders → `/orders/my`

### 2. Admin Flow
- List all users → `/users/`
- Create admin users → `/admin/users/`
- List all quotes → `/quotes/`
- Approve quote → `/quotes/{id}/status`
- Create order → `/orders/from-quote/{id}`
- List all orders → `/orders/`

### 3. Order Flow
- User retrieves:
  - `/orders/my`
  - `/orders/{id}`
- Admin retrieves:
  - `/orders/`
  - `/orders/{id}`

---

## 🧱 Project Structure

```
app/
├── main.py
├── core/
├── models/
├── schemas/
├── api/
├── services/
alembic/
requirements.txt
README.md
```

---

## 🗄️ Database

- PostgreSQL
- Managed via Alembic migrations
- Current implementation follows an MVP schema for quoting and ordering
- Orders preserve a snapshot of quote items through `order_items`

---

## ⚠️ Deployment Notes

- Hosted on Render (Free tier)
- Instance may sleep → first request can take ~50s
- Migrations are required for schema setup and updates
- The live app is deployed from GitHub through Render
  
---

## 🛠️ Local Setup

### 1. Clone repo
```bash
git clone https://github.com/HarunIsHere/repg-product-sales-quote-api.git
cd repg-product-sales-quote-api
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file with the required database and JWT settings.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your_secret_key
ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run migrations
```bash
alembic upgrade head
```

### 6. Start server
```bash
uvicorn app.main:app --reload
```

---

## 📌 Notes

- Use unique emails when testing
- Keep track of:
  - `product_id`
  - `quote_id`
  - `order_id`
- JWT must be included for protected endpoints
- Some admin listing endpoints support pagination and filtering

---

## ERD - Current Data Model (MVP)

The current system is designed as a clean MVP backend for a B2B quoting and ordering workflow. It includes users, products, quotes, and orders, with a snapshot mechanism for order items.

### Entities

#### Users
- id (int, primary key)
- full_name (string)
- email (string, unique)
- password_hash (string)
- role (customer | admin | super_admin)
- company_name (string, nullable)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)

#### Products
- id (uuid, primary key)
- name (string)
- description (string)
- price (decimal)
- sku (string, unique)
- category (string)
- stock_status (string)
- created_at (timestamp)
- updated_at (timestamp)

#### Quotes
- id (int, primary key)
- user_id (int, foreign key → users.id)
- status (pending | approved | rejected | converted)
- total_amount (decimal)
- created_at (timestamp)

#### Quote Items
- id (int, primary key)
- quote_id (int, foreign key → quotes.id)
- product_id (uuid, foreign key → products.id)
- quantity (int)
- unit_price (decimal)

#### Orders
- id (int, primary key)
- user_id (int, foreign key → users.id)
- quote_id (int, foreign key → quotes.id, unique)
- status (created)
- total_amount (decimal)
- payment_status (pending)
- created_at (timestamp)

#### Order Items (Snapshot)
- id (int, primary key)
- order_id (int, foreign key → orders.id)
- product_id (uuid, foreign key → products.id)
- quantity (int)
- unit_price (decimal)

---

### Relationships

- A user can create multiple quotes
- A quote belongs to one user
- A quote contains multiple quote_items
- Each quote_item references a product
- A quote can be converted into exactly one order
- An order belongs to one user
- An order contains multiple order_items
- Each order_item references a product

---

## Key Architectural Decision

### Order Items Snapshot

When an order is created from a quote:

- All `quote_items` are copied into `order_items`
- This ensures:
  - immutability of orders
  - auditability of past transactions
  - independence from future product or quote changes

This is a critical design choice for real-world B2B systems.

---

## Scope Note

This ERD reflects the current MVP implementation.

The following components are planned for future versions (V2), but are not yet implemented:

- addresses
- audit logs
- status history tracking
- external integrations (ERP, payment, shipping)

---

## 🏗️ Architecture

The project follows a layered backend architecture built around FastAPI, SQLAlchemy, and PostgreSQL.

### API Layer

Implemented with FastAPI route modules under `app/api/`.

Responsible for:
- exposing REST endpoints
- handling request/response flow
- applying authentication and authorization
- returning structured JSON responses

---

### Schema Layer

Implemented with Pydantic models under `app/schemas/`.

Responsible for:
- request validation
- response serialization
- enforcing input structure and data types

---

### Model Layer

Implemented with SQLAlchemy models under `app/models/`.

Responsible for:
- defining database tables
- representing business entities
- mapping Python objects to relational data

---

### Database Layer

Uses PostgreSQL with SQLAlchemy and Alembic.

Responsible for:
- persistent storage
- relational integrity
- schema versioning through migrations

---

### Security Layer

Responsible for:
- password hashing
- JWT token creation and validation
- role-based access control for protected endpoints

---

### Authentication and Authorization

Authentication is implemented with JWT tokens.

#### Workflow:

1. A user logs in with email and password  
2. The API validates credentials  
3. A JWT access token is generated  
4. Protected endpoints require that token  
5. Role checks determine access to admin-only functionality  

#### Current roles:

- customer
- admin
- super_admin

---

### Business Workflow

1. Admin or super admin creates products  
2. A customer registers and logs in  
3. The customer browses products  
4. The customer creates a quote with one or more quote items  
5. Admin or super admin reviews the quote  
6. An approved quote is converted into an order  
7. During conversion, quote items are copied into order items  
8. The order becomes an immutable transactional snapshot  

---

### Architectural Highlights

#### 1. Separation of concerns
Each major concern is kept in its own layer:
- routes in `api`
- validation in `schemas`
- persistence in `models`

#### 2. Migration-controlled schema evolution
Database schema changes are handled through Alembic migrations instead of manual edits.

#### 3. Snapshot-based ordering model
Orders do not depend on live quote items after creation.  
Instead, order items are copied during conversion.

#### 4. Role-protected write operations
Sensitive operations such as product creation, quote approval, admin user creation, and order creation are restricted to elevated roles.

---

## 🔒 Security and Data Handling

- Passwords are not stored in plain text  
- Passwords are hashed before saving to the database  
- JWT tokens are used for authenticated access  
- Protected endpoints require Bearer token authorization  
- Role-based access is enforced on admin-only routes  
- User-facing endpoints restrict access to the owner’s own data  
- Login credentials are not retrievable through the API  
- Order data is preserved as a snapshot through `order_items`  

---

## 👤 Author

Harun Ayarturk  
Backend Engineer  

GitHub:  
https://github.com/HarunIsHere

---

## 📄 License

For educational and demonstration purposes.
