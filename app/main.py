from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.routers import property
from app.database.connection import engine, Base
from app.database import models
from app.models.schemas import UserCreate, User, UserResponse, Token
from app.auth import get_password_hash, verify_password, create_access_token, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Compliance Photo Gallery API",
    description="API for managing compliance photo gallery"
)

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
