from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings


def _engine_kwargs_from_url(url: str) -> dict:
	if url.startswith("sqlite"):
		return {"connect_args": {"check_same_thread": False}}
	return {}


engine = create_engine(settings.database_url, pool_pre_ping=True, **_engine_kwargs_from_url(settings.database_url))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()