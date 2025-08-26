# Backend (FastAPI)

## Prereqs
- Python 3.11+ (3.13 works; we handle deps)
- Pip (system-managed ok)

## Install & run
```bash
cd backend
cp .env.example .env
# Adjust CORS and DB URL if needed
pip install --break-system-packages -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs

## Environment
- `DATABASE_URL`: default `sqlite:///./dsps.db`
- `BACKEND_CORS_ORIGINS`: comma-separated origins
- `WEB3_PROVIDER_URL`, `CONTRACT_ADDRESS`, `CONTRACT_PRIVATE_KEY`: enable chain writes
- `DSPS_AUTO_PUSH`: `true` to push on pass automatically

## Endpoints
- `POST /api/v1/submit`: multipart form (file, user_name, wallet_address?, skill)
- `GET /api/v1/results/{id}`: result info + tx hash if present
- `POST /api/v1/results/{id}/push`: push existing passing result on-chain
- `GET /api/v1/certificates/{id}`: download certificate PDF
- `GET /api/v1/verify/{wallet}`: read records from chain

## Files
- Uploads saved under `app/static/submissions/`
- Certificates under `app/static/certificates/`

## Common issues
- Pydantic build on Python 3.13: we pin to versions with prebuilt wheels.
- SQLAlchemy on Python 3.13: upgrade to 2.0.43+ fixed a symbol error.