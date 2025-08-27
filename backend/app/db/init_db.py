from app.models.base import Base
# Import models so SQLAlchemy sees them
from app.models import user as user_model  # noqa: F401
from app.models import submission as submission_model  # noqa: F401
from app.models import result as result_model  # noqa: F401
from app.db.session import engine


def init_db() -> None:
	Base.metadata.create_all(bind=engine)