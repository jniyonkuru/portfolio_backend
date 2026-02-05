from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from app.db.db_config import engine
from app.repositories.base_repository import ExperienceRepository
from app.models.models import  Experience,Project,Profile

def create_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(create_session)]

def create_experience_repo(session:SessionDep)->ExperienceRepository:

    return ExperienceRepository(session)
    
def common_parameters(query:str|None=None,skip:int=0,limit:int=0):
    return {"q":query,"skip":skip,"limit":limit}

CommonDep=Annotated[dict,Depends(common_parameters)]

ExperienceRepoDeps=Annotated[ExperienceRepository,Depends(create_experience_repo)]