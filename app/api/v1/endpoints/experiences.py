from fastapi import APIRouter ,HTTPException
from app.schemas.schemas import  ExperienceCreate,ExperienceDB
from app.dependencies import sessionDep
from app.services.experience_service import create_experience_service
router=APIRouter(
    prefix='/api/v1/experiences',
    tags=["Experience"],
    responses={404:{"description":"Not found"}}
)

fake_bd=[{"id":1,"company":"Andela Rwanda","role":"Web  developer","start_date":"01-01-2024","end_date":"30-11-2024"}]


@router.post('/',response_model=dict)
async def create_experience(experience:ExperienceCreate,session:sessionDep):
   new_experience= await create_experience_service (session=session,experience=experience)
   return {"message":"Record create successfully!","data":new_experience}
    


# @router.get('/',response_model=list[Experience])
# async def read_experience():
#     return fake_bd
       