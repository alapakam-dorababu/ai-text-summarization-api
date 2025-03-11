from sqlmodel import SQLModel, create_engine, Session
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


def get_db():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
