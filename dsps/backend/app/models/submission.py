from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Submission(Base):
	__tablename__ = "submissions"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
	skill: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
	code_path: Mapped[str] = mapped_column(String(512), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

	user: Mapped["User"] = relationship(back_populates="submissions")
	result: Mapped[Optional["Result"]] = relationship(
		back_populates="submission",
		uselist=False,
		cascade="all, delete-orphan",
	)