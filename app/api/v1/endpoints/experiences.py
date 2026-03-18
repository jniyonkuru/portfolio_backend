#resources from standard packages 
from typing import Annotated

#resources from  third part packages
from fastapi import APIRouter,Depends,Body,HTTPException,status


#resources from local packages 

from  app.dependencies import CommonDep
from  app.dependencies import SessionDep
from  app.models import ExperienceDB
from app.schemas import ExperienceCreate,ExperienceUpdate,Experience
from app.repositories.base_repository import ExperienceRepository
from app.services.experience_services import create_experience_service,get_experience_by_id_service,get_list_of_experiences_service,update_experience_service,delete_experience_service
from app.dependencies import ExperienceRepoDeps,auth_dependency



router=APIRouter(
    prefix='/api/v1/experiences',
    tags=["Experiences"],
    responses={404:{"description":"Not found"}}
)


@router.post("/",response_model=Experience )
async def create_experience(experience:Annotated[ExperienceCreate,Body()],repo:ExperienceRepoDeps,token:auth_dependency):
    
     return await create_experience_service(experience=experience,experience_repo=repo)
      
    
@router.get("/{id}",response_model=Experience)
async def get_experience (id:int,repo:ExperienceRepoDeps):
    return await get_experience_by_id_service(id,repo)
   
   
@router.get("/",response_model=list[Experience])
async def get_experiences(repo:ExperienceRepoDeps):
   return await  get_list_of_experiences_service(experience_repo=repo)

@router.delete("/{id}")
async def  delete_experience (id:int,repo:ExperienceRepoDeps):
    return await delete_experience_service(experience_repo=repo,id=id)

@router.put("/{id}")
async def update_experience(id:int,repo:ExperienceRepoDeps,update_experience:Annotated[ExperienceUpdate,Body()]):
    return await update_experience_service(id=id,update_experience=update_experience,experience_repo=repo)
   









       