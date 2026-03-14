from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

def train_popularity(clean_events_csv: Path) -> dict:
    """
    Popularity model = global item click counts.
    Cold-start fallback is the same list (global popularity)

    """
    df = pd.read_csv(clean_events_csv)

    # Keep only clicks (we only generate clicks today, but this is future-proof)
    df = df[df["event_type"] == "click"].copy()

    counts = (
        df.groupby("item_id", as_index=False)
        .size()
        .rename(columns={"size": "clicks"})
        .sort_values(["clicks", "item_id"], ascending=[False, True])
    )

    popular_items = counts["item_id"].tolist()

    return {
        "model_type": "popularity_v1",
        "popular_items": popular_items,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_rows": int(len(df)),
    }

def save_versioned_artifact(model: dict, artifacts_dir: Path = Path("artifacts/models")) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = artifacts_dir / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    model_path = out_dir / "model.json"
    meta_path = out_dir / "metadata.json"

    with model_path.open("w") as f:
        json.dump(model, f, indent=2)

    metadata = {
        "model_type": model.get("model_type"),
        "trained_at_utc": model.get("trained_at_utc"),
        "data_rows": model.get("data_rows")
    }
    with meta_path.open("w") as f:
        json.dump(metadata, f, indent=2)

    # Convenience pointer to latest
    latest_path = artifacts_dir / "LATEST"
    latest_path.write_text(str(out_dir))

    print(f"Saved model: {model_path}")
    print(f"Saved metadata: {meta_path}")
    print(f"Updated LATEST: {latest_path} -> {out_dir}")
    return out_dir

def main():
    clean_csv = Path("data/clean/events.csv")
    if not clean_csv.exists():
        raise FileNotFoundError("Missing data/clean/events.csv. Run generate_events first.")
    
    model = train_popularity(clean_csv)
    save_versioned_artifact(model)

if __name__ == "__main__":
    main()

    
