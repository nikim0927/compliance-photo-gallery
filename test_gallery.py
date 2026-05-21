from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import SessionLocal
from app.database import models

client = TestClient(app)
db = SessionLocal()

prop = models.Property(address="123", realtor_id=1, price=10.0)
db.add(prop)
db.commit()
db.refresh(prop)

try:
    response = client.get(f"/gallery/{prop.id}")
    print("Status:", response.status_code)
    if response.status_code == 500:
        print("Error text:", response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
