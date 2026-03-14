# src/recsys/generate_events.py

import random
from pathlib import Path
from datetime import datetime, timedelta, timezone

import pandas as pd


# This file MAKES fake user click events and saves them to CSV files

def generate_events(n_users=5, n_items=20, n_events=200, seed=7):
    random.seed(seed)

    users = [f"u{u}" for u in range(1, n_users + 1)]
    items = [f"i{i}" for i in range(1, n_items + 1)]

    # Make early items more likely to be clicked (so "popularity" exists)

    weights = [1.0 / (i ** 0.7) for i in range(1, n_items + 1)]
    total = sum(weights)
    probs = [w / total for w in weights]

    start = datetime.now(timezone.utc) - timedelta(days=3)

    rows = []

    for t in range(n_events):
        user_id = random.choice(users)
        item_id = random.choices(items, weights=probs, k=1)[0]
        ts = start + timedelta(minutes=t * random.randint(1, 3))
        rows.append({
            "user_id": user_id,
            "item_id": item_id,
            "event_type": "click",
            "ts": ts.isoformat(),
        })

    df = pd.DataFrame(rows).sort_values("ts").reset_index(drop=True)
    return df

def main() -> None:
    raw_path = Path("data/raw/events.csv")
    clean_path = Path("data/clean/events.csv")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_events()
    df.to_csv(raw_path, index=False)

    # "Cleaned" boundary: for now, we just copy raw -> clean.
    # Later we will enforce schema, dedup, filtering, etc.
    df.to_csv(clean_path, index=False)

    print(f"Wrote raw:  {raw_path} ({len(df)} rows)")
    print(f"Wrote clean: {clean_path} ({len(df)} rows)")
    print(f"First ts: {df['ts'].iloc[0]}")
    print(f"Last ts: {df['ts'].iloc[-1]}")

if __name__ == "__main__":
    main()
