from fastapi.testclient import TestClient

from app.src.main import app

client = TestClient(app)
