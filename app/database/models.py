from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database.connection import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    realtor_id = Column(Integer, index=True)
    price = Column(Float)

    image_pairs = relationship("ImagePair", back_populates="property")


class ImagePair(Base):
    __tablename__ = "image_pairs"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    original_url = Column(String)
    edited_url = Column(String)
    alteration_type = Column(String)
    is_structural_change = Column(Boolean, default=False)
    ai_confidence_score = Column(Float)
    compliance_id = Column(String, index=True)

    property = relationship("Property", back_populates="image_pairs")
