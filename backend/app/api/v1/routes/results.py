from pathlib import Path
from typing import List, Optional
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Result, User, Submission
from app.services.certificates.generator import CertificateGenerator
from app.services.blockchain.client import DSPSBlockchainClient

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


@router.post("/results/{result_id}/push")
def push_result_on_chain(result_id: int, db: Session = Depends(get_db)) -> dict:
	res = db.query(Result).filter(Result.id == result_id).first()
	if not res:
		raise HTTPException(status_code=404, detail="Result not found")
	if not res.passed:
		raise HTTPException(status_code=400, detail="Only passing results can be pushed on-chain")
	user = db.query(User).filter(User.id == res.user_id).first()
	if not user or not user.wallet_address:
		raise HTTPException(status_code=400, detail="User wallet address is required to push on-chain")

	try:
		client = DSPSBlockchainClient.from_env()
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Blockchain client not configured: {e}")

	from time import time
	try:
		tx_hash = client.add_record(user_address=user.wallet_address, skill=res.skill, score=res.score, timestamp=int(time()))
		res.blockchain_tx_hash = tx_hash
		db.add(res)
		db.commit()
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to push on-chain: {e}")

	# Regenerate certificate with hash
	cert_dir = "/workspace/dsps/backend/app/static/certificates"
	cg = CertificateGenerator(cert_dir)
	cert = cg.generate_certificate(user_name=user.name, skill=res.skill, score=res.score, blockchain_tx_hash=res.blockchain_tx_hash, filename_prefix=f"result_{res.id}")

	return {"result_id": res.id, "tx_hash": res.blockchain_tx_hash, "certificate": str(cert)}


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


@router.get("/verify/{wallet_address}")
def verify_on_chain(wallet_address: str) -> dict:
	from app.services.blockchain.client import DSPSBlockchainClient
	import os
	if not (os.getenv("WEB3_PROVIDER_URL") and os.getenv("CONTRACT_ADDRESS") and os.getenv("CONTRACT_PRIVATE_KEY")):
		raise HTTPException(status_code=500, detail="Blockchain client not configured on server")
	try:
		client = DSPSBlockchainClient.from_env()
		records = client.get_records(wallet_address)
		return {"wallet_address": wallet_address, "records": records}
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to fetch on-chain records: {e}")