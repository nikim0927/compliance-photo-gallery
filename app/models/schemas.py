from pydantic import BaseModel

class ImagePairCreate(BaseModel):
    original_url: str
    edited_url: str
    alteration_type: str
    is_structural_change: bool = False
    ai_confidence_score: float
    compliance_id: str

class ImagePair(ImagePairCreate):
    id: int
    property_id: int

    class Config:
        from_attributes = True

class PropertyCreate(BaseModel):
    address: str
    realtor_id: int
    price: float

class Property(PropertyCreate):
    id: int

    class Config:
        from_attributes = True
