import logging
from logging.config import dictConfig

from app.core.config import settings


def configure_logging() -> None:
	# Minimal, structured-enough logging for MVP
	log_level = settings.get_log_level()
	dictConfig({
		"version": 1,
		"disable_existing_loggers": False,
		"formatters": {
			"default": {
				"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
			}
		},
		"handlers": {
			"console": {
				"class": "logging.StreamHandler",
				"formatter": "default",
				"level": log_level,
			}
		},
		"root": {
			"handlers": ["console"],
			"level": log_level,
		},
	})
	logging.getLogger(__name__).debug("Logging configured")