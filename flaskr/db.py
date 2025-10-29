import sys
from typing import Callable

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .models import Base


def create_db_session(database_url: str) -> tuple[scoped_session[Session], Callable]:
    engine = create_engine(database_url)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    def remove_session(_exc=None):
        db_session.remove()

    return (db_session, remove_session)


def get_db_session() -> scoped_session[Session]:
    return current_app.config["DB_SESSION"]


def init_db(database_url: str):
    engine = create_engine(database_url, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db(sys.argv[1])
