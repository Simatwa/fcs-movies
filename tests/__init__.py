from fastapi.testclient import TestClient
from backend import app

client = TestClient(
    app,
)
