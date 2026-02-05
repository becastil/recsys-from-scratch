from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

def test_end_to_end_smoke() -> None: 
    # 1) data exists
    assert Path("data/clean/events.csv").exists(), "Run: python src/recsys/generate_events.py"
    # 2) model exists 
    assert Path("artifacts/models/LATEST").exists(), "Run: python src/recsys/train_popularity.py"

    # 3) API returns k items
    with TestClient(app) as client: 
        r = client.get("/recommend", params={"user_id": "u1", "k": 5})
        assert r.status_code == 200
        payload = r.json()
        assert payload["user_id"] == "u1"
        assert len(payload["items"]) == 5
        assert all(isinstance(x, str) for x in payload["items"])

        