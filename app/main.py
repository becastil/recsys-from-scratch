import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, Query

# This file is the WEB SERVER (API).
# It loads the latest model and returns recommendations.

app = FastAPI(title="Recsys MVP (Popularity)")

ARTIFACTS_ROOT = Path("artifacts/models")
MODEL = None

def load_latest_model() -> dict: 
    latest_ptr = ARTIFACTS_ROOT / "LATEST"
    if not latest_ptr.exists():
        raise FileNotFoundError("No model found. Train one first (python src/recsys/train_popularity.py).")

    model_dir = Path(latest_ptr.read_text().strip())
    model_path = model_dir / "model.json"
    with model_path.open() as f:
        return json.load(f)

@app.on_event("startup")
def _startup() -> None:
    global MODEL
    MODEL = load_latest_model()    

@app.get("/health")
def health() -> dict:
    return {"ok": True, "model_loaded": MODEL is not None}

@app.get("/recommend")
def recommend(user_id: str = Query(...), k: int = Query(5, ge=1, le=50)) -> dict:
    # Cold-start fallback for now = same popularity list for everyone.
    if MODEL is None:
        return {"user_id": user_id, "items": [], "reason": "model_not_loaded"}
    
    items: List[str] = MODEL["popular_items"][:k]
    return {"user_id": user_id, "items": items, "model_type": MODEL["model_type"]}

