
#resources from third part packages

from typing import Annotated,Type,TypeVar
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer



#resources from  local packages

from app.db.db_config import engine
from app.repositories.base_repository import ExperienceRepository,ProfileRepository,Repo,ProjectRepository,UserRepository
from app.db.session import create_session

oauth2_scheme=OAuth2PasswordBearer('token')

T=TypeVar("T", bound=Repo)

SessionDep = Annotated[Session, Depends(create_session)]

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
UserRepoDeps=Annotated[UserRepository,Depends(get_repo(UserRepository))]


# Authentication dependencies 

auth_dependency=Annotated[str,Depends(oauth2_scheme)]

