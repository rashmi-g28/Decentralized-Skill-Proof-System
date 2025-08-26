from typing import Optional, List
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User, Submission, Result
from app.schemas.submission import SubmissionCreate, EvaluationResponse, EvaluationDetail
from app.services.evaluator.runner import CodeEvaluator
from app.services.certificates.generator import CertificateGenerator
from app.utils.file_storage import save_uploadfile, ensure_dir

router = APIRouter()

SUBMISSIONS_DIR = "/workspace/dsps/backend/app/static/submissions"
TESTCASES_DIR = "/workspace/dsps/backend/app/services/evaluator/testcases"
CERTS_DIR = "/workspace/dsps/backend/app/static/certificates"

# Ensure directories exist
ensure_dir(SUBMISSIONS_DIR)
ensure_dir(CERTS_DIR)


def _get_or_create_user(db: Session, name: str, wallet_address: Optional[str]) -> User:
	if wallet_address:
		u = db.query(User).filter(User.wallet_address == wallet_address).first()
		if u:
			# Update name if changed
			if u.name != name:
				u.name = name
				db.add(u)
				db.commit()
				db.refresh(u)
			return u
	# Fallback: create a new user record
	u = User(name=name, wallet_address=wallet_address)
	db.add(u)
	db.commit()
	db.refresh(u)
	return u


@router.post("/submit", response_model=EvaluationResponse)
async def submit_code(
	file: UploadFile = File(..., description="Python file containing solve(input) function"),
	user_name: str = Form(...),
	wallet_address: Optional[str] = Form(None),
	skill: str = Form(...),
	db: Session = Depends(get_db),
):
	if not file.filename.endswith(".py"):
		raise HTTPException(status_code=400, detail="Only .py files are accepted")

	user = _get_or_create_user(db, user_name, wallet_address)
	# Save uploaded file
	code_path = save_uploadfile(file, SUBMISSIONS_DIR, extension=".py")

	# Create submission record
	sub = Submission(user_id=user.id, skill=skill, code_path=str(code_path))
	db.add(sub)
	db.commit()
	db.refresh(sub)

	# Evaluate code
	evaluator = CodeEvaluator(TESTCASES_DIR)
	try:
		result = evaluator.evaluate(skill=skill, user_code_path=str(code_path))
	except FileNotFoundError as e:
		raise HTTPException(status_code=400, detail=str(e))

	# Store result
	res = Result(
		user_id=user.id,
		submission_id=sub.id,
		skill=skill,
		score=result.score,
		passed=result.passed_overall,
		blockchain_tx_hash=None,
	)
	db.add(res)
	db.commit()
	db.refresh(res)

	certificate_path: Optional[str] = None
	if res.passed:
		# Generate certificate now (blockchain hash may be added later)
		cg = CertificateGenerator(CERTS_DIR)
		cert = cg.generate_certificate(
			user_name=user.name,
			skill=skill,
			score=result.score,
			blockchain_tx_hash=res.blockchain_tx_hash,
			filename_prefix=f"result_{res.id}",
		)
		certificate_path = str(cert)

	# Prepare response
	details_models: List[EvaluationDetail] = [EvaluationDetail(**d) for d in result.details]
	return EvaluationResponse(
		skill=skill,
		total=result.total,
		passed=result.passed,
		score=result.score,
		passed_overall=result.passed_overall,
		details=details_models,
		submission_id=sub.id,
		result_id=res.id,
	)