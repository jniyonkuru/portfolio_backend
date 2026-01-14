from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from app.db.db_config import engine

def create_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(create_session)]