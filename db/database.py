from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from core.config import url

Base = declarative_base()
engine = create_engine(url, echo=True)


if not database_exists(engine.url):
    try:
        create_database(engine.url)
    except Exception as e:
        print(f"error: {e}")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
