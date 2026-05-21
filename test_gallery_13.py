from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.database import models

client = TestClient(app)
db = SessionLocal()

prop = models.Property(id=13, address="13 Debug Ave", realtor_id=1, price=None)
db.merge(prop)
db.commit()

pair = models.ImagePair(
    property_id=13,
    original_url="uploads/test1.jpg",
    edited_url="uploads/test2.jpg",
    alteration_type="Test",
    is_structural_change=True,
    ai_confidence_score=None,
    compliance_id="COMP13"
)
db.add(pair)
db.commit()

try:
    response = client.get(f"/gallery/13")
    print("Status:", response.status_code)
    if response.status_code == 500:
        print("Error text:", response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
