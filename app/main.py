from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI(title="RePG Product, Sales & Quote Management API")

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "RePG API is running"}
