# RePG Product, Sales & Quote Management API

Backend API for managing products, quotes, and orders for RePG’s B2B operations.

---

## 🚀 Live API

Swagger Docs:  
https://repg-product-sales-quote-api.onrender.com/docs

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

---

## 📦 Features

- User authentication (JWT)
- Role-based access:
  - User
  - Admin
  - Super Admin
- Product management
- Quote creation & tracking
- Order creation from approved quotes
- Status workflow (quotes → orders)

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

### 2. Admin Flow
- Approve quote → `/quotes/{id}/status`
- Create order → `/orders/from-quote/{id}`

### 3. Order Flow
- User retrieves:
  - `/orders/my`
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
```

---

## 🗄️ Database

- PostgreSQL
- Managed via Alembic migrations

---

## ⚠️ Deployment Notes

- Hosted on Render (Free tier)
- Instance may sleep → first request can take ~50s
- Migrations executed via:
  ```bash
  alembic upgrade head
  ```

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

### 4. Run migrations
```bash
alembic upgrade head
```

### 5. Start server
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

---

## 👤 Author

Harun Ayarturk  
Backend Engineer  

GitHub:  
https://github.com/HarunIsHere

---

## 📄 License

For educational and demonstration purposes.
