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

def save_versioned_artifact(model: )