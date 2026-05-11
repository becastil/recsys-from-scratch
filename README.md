# recsys-from-scratch

A minimal end-to-end recommender system built from the ground up — no recommender libraries, just `pandas` + `scikit-learn` + `FastAPI`. The point isn't beating a benchmark; it's understanding every piece of the pipeline (data → model → artifacts → API → recommendations) without leaning on a black-box library.

## What's here

```
src/recsys/
  generate_events.py   – produce synthetic user-item interaction events
  train_popularity.py  – train a popularity-baseline model + persist a versioned artifact
app/
  main.py              – FastAPI service that loads the latest model and serves /recommendations
tests/
  test_smoke.py        – sanity check that train + serve hang together
```

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. generate some synthetic events
python -m src.recsys.generate_events

# 2. train the popularity baseline and write a versioned artifact
python -m src.recsys.train_popularity

# 3. start the API
uvicorn app.main:app --reload

# 4. ask for recommendations
curl 'http://localhost:8000/recommendations?user_id=1&k=5'
```

## Tech

Python 3.10+ · pandas · scikit-learn · FastAPI · uvicorn · pytest

## Status

Popularity baseline only — the simplest model that still requires the full pipeline. Future work would swap in collaborative filtering (matrix factorization) using the same artifact-versioning + API contract.
