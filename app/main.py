from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routers import property
from app.database.connection import engine, Base, get_db
from app.database import models
from app.models.schemas import UserCreate, User, UserResponse, Token
from app.auth import get_password_hash, verify_password, create_access_token, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Compliance Photo Gallery API",
    description="API for managing compliance photo gallery"
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="app/templates")

app.include_router(property.router)

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        realtor_license_number=user.realtor_license_number
    )
    fake_users_db[user.username] = db_user
    return db_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Compliance Photo Gallery API is running"}

@app.get("/gallery/{property_id}")
def gallery(property_id: int, request: Request, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    image_pairs = db_property.image_pairs
    
    realtor_license_number = "CA-987654"
    realtor_logo_url = None

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "property": db_property,
            "image_pairs": image_pairs,
            "realtor_license_number": realtor_license_number,
            "realtor_logo_url": realtor_logo_url
        }
    )
