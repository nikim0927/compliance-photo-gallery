from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import Property, PropertyCreate
from app.database import models
from app.database.connection import get_db

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.post("/", response_model=Property)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property
