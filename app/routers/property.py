from fastapi import APIRouter
from app.models.schemas import Property

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int):
    # Return dummy property data
    return Property(
        id=property_id,
        address=f"{property_id} Main St",
        realtor_id=999,
        price=500000.0
    )
