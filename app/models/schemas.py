from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    realtor_license_number: str

class User(BaseModel):
    username: str
    hashed_password: str
    realtor_license_number: str

class UserResponse(BaseModel):
    username: str
    realtor_license_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

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

class ImagePairResponse(BaseModel):
    image_pair: ImagePair
    disclosure: str

class PropertyCreate(BaseModel):
    address: str
    realtor_id: int
    price: float

class Property(PropertyCreate):
    id: int

    class Config:
        from_attributes = True
