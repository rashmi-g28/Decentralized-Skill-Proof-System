from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.db.init_db import init_db
from app.api.v1.routes import health


# Configure logging early so startup logs are formatted
configure_logging()

app = FastAPI(
	title="DSPS Backend",
	version="0.1.0",
	docs_url="/docs",
	openapi_url="/openapi.json",
)

# Allow local dev frontends (Vite, etc.). Update via BACKEND_CORS_ORIGINS in .env
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.get_cors_origins(),
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
	# Ensure DB tables exist (safe to call repeatedly)
	init_db()


# Mount versioned API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"]) 


@app.get("/")
def read_root() -> dict:
	return {
		"message": "DSPS Backend is running",
		"docs": "/docs",
	}