
#resources from third part packages

from typing import Annotated,Type,TypeVar
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


#resources from  local packages

from app.db.db_config import engine
from app.repositories.base_repository import ExperienceRepository,ProfileRepository,Repo,ProjectRepository
from app.db.session import create_session

T=TypeVar("T", bound=Repo)

SessionDep = Annotated[AsyncSession, Depends(create_session)]

def get_repo(cls:Type[T]):
    def _get_repo(session:SessionDep)->T:
          return cls(session=session)
    return _get_repo
def common_parameters(query:str|None=None,skip:int=0,limit:int=0):
    return {"q":query,"skip":skip,"limit":limit}

CommonDep=Annotated[dict,Depends(common_parameters)]

ExperienceRepoDeps=Annotated[ExperienceRepository,Depends(get_repo(ExperienceRepository))]
ProjectRePoDeps=Annotated[ProjectRepository,Depends(get_repo(ProjectRepository))]
ProfileRepoDeps=Annotated[ProfileRepository,Depends(get_repo(ProfileRepository))]