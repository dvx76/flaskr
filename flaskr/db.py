from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base

engine = create_engine("sqlite:///flaskr.sqlite")
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def close_db(_exc=None):
    db_session.remove()


def init_db(database: str = "sqlite:///flaskr.sqlite"):
    engine = create_engine(database, echo=True)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
