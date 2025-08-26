from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Result(Base):
	__tablename__ = "results"
	__table_args__ = (
		Index("ix_results_user_skill", "user_id", "skill"),
	)

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
	submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id", ondelete="CASCADE"), index=True, nullable=False)
	skill: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
	score: Mapped[int] = mapped_column(Integer, nullable=False)
	passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	blockchain_tx_hash: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

	user: Mapped["User"] = relationship(back_populates="results")
	submission: Mapped["Submission"] = relationship(back_populates="result")