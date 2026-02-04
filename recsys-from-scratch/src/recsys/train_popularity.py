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

    

