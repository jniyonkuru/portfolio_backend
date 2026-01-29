from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from app.db.db_config import engine
from .repositories.base_repository import BaseRepository
from .models.models import  Experience,Project

def create_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(create_session)]

def create_experience_repo(session:SessionDep):
          
    return BaseRepository(Experience,session)
    


def common_parameters(query:str|None=None,skip:int=0,limit:int=0):
    return {"q":query,"skip":skip,"limit":limit}

CommonDep=Annotated[dict,Depends(common_parameters)]