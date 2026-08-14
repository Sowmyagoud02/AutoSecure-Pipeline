from backend.database.session import engine
from backend.models.base import Base
from backend.models.user import User
from backend.models.ingestion import Ingestion


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()