from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router

app = FastAPI(title="RePG Product, Sales & Quote Management API")

app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "RePG API is running"}
