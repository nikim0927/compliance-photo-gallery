from fastapi import FastAPI
from app.routers import property

app = FastAPI(
    title="Compliance Photo Gallery API",
    description="API for managing compliance photo gallery"
)

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Compliance Photo Gallery API is running"}
