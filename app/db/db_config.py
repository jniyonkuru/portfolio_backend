from sqlmodel import create_engine,Session,SQLModel
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "sqlite:///./portfolio.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_session():
    with Session(engine) as session:
        yield session

    #create  database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

sessionDep=Annotated[Session,Depends(create_session)]