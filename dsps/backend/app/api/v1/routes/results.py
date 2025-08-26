from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Result, User, Submission

router = APIRouter()


@router.get("/results/{result_id}")
def get_result(result_id: int, db: Session = Depends(get_db)) -> dict:
	res = db.query(Result).filter(Result.id == result_id).first()
	if not res:
		raise HTTPException(status_code=404, detail="Result not found")
	user = db.query(User).filter(User.id == res.user_id).first()
	return {
		"id": res.id,
		"user_name": user.name if user else None,
		"wallet_address": user.wallet_address if user else None,
		"skill": res.skill,
		"score": res.score,
		"passed": res.passed,
		"blockchain_tx_hash": res.blockchain_tx_hash,
	}


@router.get("/results/by_user/{wallet_address}")
def get_results_by_wallet(wallet_address: str, db: Session = Depends(get_db)) -> List[dict]:
	user = db.query(User).filter(User.wallet_address == wallet_address).first()
	if not user:
		return []
	rows = db.query(Result).filter(Result.user_id == user.id).order_by(Result.id.desc()).all()
	return [
		{
			"id": r.id,
			"skill": r.skill,
			"score": r.score,
			"passed": r.passed,
			"blockchain_tx_hash": r.blockchain_tx_hash,
		}
		for r in rows
	]


@router.get("/certificates/{result_id}")
def download_certificate(result_id: int, db: Session = Depends(get_db)):
	# Certificate files are named result_{id}_*.pdf under static/certificates
	cert_dir = Path("/workspace/dsps/backend/app/static/certificates")
	pattern = f"result_{result_id}_"
	candidates = list(cert_dir.glob(f"{pattern}*.pdf"))
	if not candidates:
		raise HTTPException(status_code=404, detail="Certificate not found")
	path = candidates[0]
	return FileResponse(path, media_type="application/pdf", filename=path.name)