from fastapi import APIRouter,Depends,Body,HTTPException,status
from  app.dependencies import CommonDep
from  app.dependencies import SessionDep
from  app.models.models import Experience
from app.schemas.schemas import ExperienceCreate,ExperienceUpdate
from typing import Annotated
from app.repositories.base_repository import ExperienceRepository
from app.services.experience_services import create_experience_service,get_experience_by_id_service,get_list_of_experiences_service,update_experience_service,delete_experience_service
from app.dependencies import ExperienceRepoDeps
router=APIRouter(
    prefix='/api/v1/experiences',
    tags=["Experiences"],
    responses={404:{"description":"Not found"}}
)


@router.post("/" )
async def create_experience(experience:Annotated[ExperienceCreate,Body()],repo:ExperienceRepoDeps):
    
     return create_experience_service(experience=experience,experience_repo=repo)
      
    
@router.get("/{id}",response_model=Experience)
async def get_experience (id:int,repo:ExperienceRepoDeps):
    return get_experience_by_id_service(id,repo)
   
   
@router.get("/",response_model=list[Experience])
async def get_experiences(repo:ExperienceRepoDeps):
   return  get_list_of_experiences_service(experience_repo=repo)

@router.delete("/{id}")
async def  delete_experience (id:int,repo:ExperienceRepoDeps):
    return delete_experience_service(experience_repo=repo,id=id)

@router.put("/{id}")
async def update_experience(id:int,repo:ExperienceRepoDeps,update_experience:Annotated[ExperienceUpdate,Body()]):
    return update_experience_service(id=id,update_experience=update_experience,experience_repo=repo)
   









       