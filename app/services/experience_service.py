from fastapi import Depends,HTTPException,status
from ..dependencies import sessionDep
from typing import Annotated
from sqlmodel import Session,select
from ..schemas.schemas import ExperienceDB,ExperienceCreate

async def get_experiences_service(session:Session,limit:int=100,skip:int=0) -> list[ExperienceDB]:
    try:
        query = select(ExperienceDB).limit(limit).offset(skip)
        results = session.exec(query).all()
        return list(results)
    except   Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

async def get_experience_by_id_service(session:Session,experience_id:int) -> ExperienceDB:
   
   try:
    experience =session.get(ExperienceDB,id)
    if not experience:
       raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Experience with the given id was not found")
    return experience
   except Exception as e :
     raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e)) from e
   

async def create_experience_service (session:Session,experience:ExperienceCreate):
     
     try:

       experience_exists=session.exec(select(ExperienceDB).where(ExperienceDB.organization == experience.organization and ExperienceDB.role == experience.role ))

       if experience_exists != None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail="Record already exists")
      
       new_experience = session.add(experience)
       return  new_experience
     except Exception as e:
          raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e)) from e

      
    