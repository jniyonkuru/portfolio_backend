from fastapi import APIRouter,Depends,Body,HTTPException,status
from  app.dependencies import CommonDep
from  app.dependencies import SessionDep,create_experience_repo
from  app.models.models import Experience
from app.schemas.schemas import ExperienceCreate
from typing import Annotated
from app.repositories.base_repository import BaseRepository
from app.services.experience_services import create_experience_service
router=APIRouter(
    prefix='/api/v1/experiences',
    tags=["Experience"],
    responses={404:{"description":"Not found"}}
)
ExperienceRepoDeps=Annotated[BaseRepository[Experience],Depends(create_experience_repo)]

@router.post("/" ,response_model=Experience)
async def  create_experience(experience:Annotated[ExperienceCreate,Body()],repo:ExperienceRepoDeps):
    try :
      new_experience= create_experience_service(experience=experience,experience_repo=repo)
      return new_experience
    except HTTPException:
       raise
    except Exception as e:
       raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))









       