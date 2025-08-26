from fastapi import APIRouter

from app.utils.time import now_utc_iso

router = APIRouter()


@router.get("/healthz")
def healthcheck() -> dict:
	return {
		"status": "ok",
		"time": now_utc_iso(),
	}