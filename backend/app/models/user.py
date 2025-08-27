from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String(100), nullable=False)
	wallet_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, unique=True, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

	submissions: Mapped[List["Submission"]] = relationship(
		back_populates="user",
		cascade="all, delete-orphan",
	)
	results: Mapped[List["Result"]] = relationship(
		back_populates="user",
		cascade="all, delete-orphan",
	)