from fastapi import FastAPI

app = FastAPI(
    title="Compliance Photo Gallery API",
    description="API for managing compliance photo gallery"
)

@app.get("/")
def read_root():
    return {"message": "Compliance Photo Gallery API is running"}
