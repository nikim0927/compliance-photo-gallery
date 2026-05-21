import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.schemas import Property, PropertyCreate, ImagePair, ImagePairCreate, ImagePairResponse, DescriptionRequest
from app.database import models
from app.database.connection import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.post("/", response_model=Property)
def create_property(property: PropertyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
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

@router.post("/{property_id}/upload-pair", response_model=ImagePair)
def upload_image_pair(property_id: int, image_pair: ImagePairCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db_image_pair = models.ImagePair(**image_pair.model_dump(), property_id=property_id)
    db.add(db_image_pair)
    db.commit()
    db.refresh(db_image_pair)
    return db_image_pair

@router.post("/{property_id}/upload-files", response_model=ImagePairResponse)
def upload_image_files(
    property_id: int,
    original_file: UploadFile = File(...),
    edited_file: UploadFile = File(...),
    alteration_type: str = Form(...),
    is_structural_change: bool = Form(...),
    ai_confidence_score: float = Form(...),
    compliance_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not (0 <= ai_confidence_score <= 1):
        raise HTTPException(status_code=400, detail="ai_confidence_score must be between 0 and 1")

    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    os.makedirs("uploads", exist_ok=True)
    
    orig_path = f"uploads/{original_file.filename}"
    with open(orig_path, "wb") as buffer:
        shutil.copyfileobj(original_file.file, buffer)
        
    edit_path = f"uploads/{edited_file.filename}"
    with open(edit_path, "wb") as buffer:
        shutil.copyfileobj(edited_file.file, buffer)

    db_image_pair = models.ImagePair(
        property_id=property_id,
        original_url=orig_path,
        edited_url=edit_path,
        alteration_type=alteration_type,
        is_structural_change=is_structural_change,
        ai_confidence_score=ai_confidence_score,
        compliance_id=compliance_id
    )
    db.add(db_image_pair)
    db.commit()
    db.refresh(db_image_pair)
    
    disclosure = "In accordance with CA AB 723, certain images have been digitally altered. Original unedited source files are available for transparency and compliance review."
    
    return {"image_pair": db_image_pair, "disclosure": disclosure}

@router.get("/{property_id}/image-pairs", response_model=list[ImagePair])
def get_image_pairs(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return db_property.image_pairs

@router.post("/{property_id}/generate-description")
def generate_description(property_id: int, request: DescriptionRequest, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    address = db_property.address
    features_str = ", ".join(request.features) if request.features else "several high-end amenities"
    
    desc = f"Welcome to the exquisite luxury property at {address}. This stunning estate boasts highly sought-after features including {features_str}. Elegantly designed with unparalleled attention to detail, this home offers a perfect blend of modern sophistication and timeless charm. From the spacious open-concept living areas to the meticulously landscaped grounds, every aspect of this property has been crafted for the ultimate luxury lifestyle. Experience comfort, privacy, and prestige in this magnificent residence. Your dream home awaits."
    
    return {"description": desc}

@router.post("/{property_id}/audit-compliance")
def audit_compliance(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    manual_review_required = False
    structural_keywords = ["removed wall", "changed window", "removed power line", "structural edit"]
    
    for pair in db_property.image_pairs:
        if not pair.is_structural_change:
            alt_type = (pair.alteration_type or "").lower()
            for kw in structural_keywords:
                if kw in alt_type:
                    manual_review_required = True
                    break
        if manual_review_required:
            break
            
    return {"manual_review_required": manual_review_required}
