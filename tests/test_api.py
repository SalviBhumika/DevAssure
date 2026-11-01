from fastapi.testclient import TestClient
from devassure.api import app
client=TestClient(app)
def test_health(): assert client.get("/health").status_code==200
def test_analyze():
    res=client.post("/analyze",json={"specification":"The API must reject invalid input."})
    assert res.status_code==200 and res.json()["test_proposals"]
