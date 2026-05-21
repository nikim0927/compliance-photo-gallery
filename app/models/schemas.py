from pydantic import BaseModel

class PropertyCreate(BaseModel):
    address: str
    realtor_id: int
    price: float

class Property(PropertyCreate):
    id: int

    class Config:
        from_attributes = True
