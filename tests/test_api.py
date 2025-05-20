from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_review_code_basic():
    payload = {
        "code": "def myFunc():\n  print('hi')",
        "language": "python"
    }
    response = client.post("/review", json=payload)

    assert response.status_code == 200
    json_data = response.json()

    assert "review" in json_data
    assert isinstance(json_data["review"], str)
    assert len(json_data["review"].strip()) > 0

    # Optional checks if you implemented extended output
    if "suggested_fix" in json_data:
        assert isinstance(json_data["suggested_fix"], (str, type(None)))

    if "score" in json_data:
        assert json_data["score"] is None or (0.0 <= json_data["score"] <= 1.0)

