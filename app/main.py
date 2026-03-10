from fastapi import FastAPI

app = FastAPI(title="RePG Product, Sales & Quote Management API")


@app.get("/")
def root():
    return {"message": "RePG API is running"}
