from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = (
    "postgresql://postgres:postgres123@localhost:5432/jkn_sentinel"
)


engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    bind=engine
)


def get_session():

    return SessionLocal()