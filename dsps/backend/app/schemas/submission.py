from typing import List, Optional
from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
	user_name: str = Field(..., description="Display name of the user")
	wallet_address: Optional[str] = Field(None, description="Optional wallet address")
	skill: str = Field(..., description="Skill identifier, e.g., 'fibonacci'")


class EvaluationDetail(BaseModel):
	case: str
	input: object
	expected: object
	got: object | None
	error: str | None
	pass_: bool = Field(alias="pass")

	class Config:
		populate_by_name = True


class EvaluationResponse(BaseModel):
	skill: str
	total: int
	passed: int
	score: int
	passed_overall: bool
	details: List[EvaluationDetail]
	submission_id: int
	result_id: int


class ResultRead(BaseModel):
	id: int
	user_name: str
	wallet_address: Optional[str]
	skill: str
	score: int
	passed: bool
	blockchain_tx_hash: Optional[str]