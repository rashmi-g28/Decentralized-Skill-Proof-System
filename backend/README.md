# DSPS Backend (FastAPI)

This is the backend API for the Decentralized Skill Proof System (DSPS). It exposes endpoints to submit code, evaluate it, store results, push records on-chain, and generate PDF certificates.

## Quick start (local)

1. Create a virtualenv and install dependencies:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

2. Run the API server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Open the interactive docs:

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Configuration

- Edit `.env` to customize the database and CORS origins.
- Default DB is SQLite at `sqlite:///./dsps.db` in the backend folder.

## Docker

```bash
cd backend
docker build -t dsps-backend:dev .
# Run container
docker run -p 8000:8000 --env-file .env dsps-backend:dev
```

## Project structure (backend)

```
backend/
  app/
    api/v1/routes/health.py
    core/config.py
    core/logging_config.py
    db/session.py
    db/init_db.py
    models/base.py
    utils/time.py
  main.py
  requirements.txt
```

This is an MVP scaffold. We'll add evaluator, blockchain client, endpoints, and certificate generation next.