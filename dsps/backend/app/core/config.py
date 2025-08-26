from typing import List
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	env: str = "local"
	database_url: str = "sqlite:///./dsps.db"
	backend_cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
	log_level: str = "INFO"

	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

	def get_cors_origins(self) -> List[str]:
		if not self.backend_cors_origins:
			return ["*"]
		return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

	def get_log_level(self) -> int:
		level = getattr(logging, self.log_level.upper(), logging.INFO)
		if isinstance(level, int):
			return level
		return logging.INFO


settings = Settings()