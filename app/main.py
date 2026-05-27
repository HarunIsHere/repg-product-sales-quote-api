from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin_users import router as admin_users_router
from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.users import router as users_router
from app.core.bootstrap import seed_first_superadmin
from app.db.session import SessionLocal
from app.api.quotes import router as quotes_router
from app.api.orders import router as orders_router

app = FastAPI(title="RePG Product, Sales & Quote Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ayartuerk.me",
        "https://frontend.ayartuerk.me",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(admin_users_router)
app.include_router(quotes_router)
app.include_router(orders_router)


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
