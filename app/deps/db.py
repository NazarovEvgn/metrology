from collections.abc import Generator

from sqlalchemy.orm import Session

from ..db import SessionLocal


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
