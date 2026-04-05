from fastapi import FastAPI

from app.api.admin_users import router as admin_users_router
from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.users import router as users_router
from app.core.bootstrap import seed_first_superadmin
from app.db.session import SessionLocal

app = FastAPI(title="RePG Product, Sales & Quote Management API")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(admin_users_router)


@app.on_event("startup")
def startup_seed_superadmin():
    db = SessionLocal()
    try:
        seed_first_superadmin(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "RePG API is running"}
