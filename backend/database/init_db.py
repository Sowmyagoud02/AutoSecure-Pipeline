from backend.database.session import engine
from backend.models.base import Base
from backend.models.user import User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)