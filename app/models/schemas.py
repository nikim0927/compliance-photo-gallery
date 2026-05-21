from pydantic import BaseModel

class Property(BaseModel):
    id: int
    address: str
    realtor_id: int
    price: float
