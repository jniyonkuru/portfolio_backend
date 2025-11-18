from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel

router=APIRouter(
    prefix='/experiences',
    tags=["Experience"],
    responses={404:{"description":"Not found"}}
)

class Experience(BaseModel):
    id:int
    company:str
    role:str
    start_date:str
    end_date:str



fake_bd=[{"id":1,"company":"Andela Rwanda","role":"Web  developer","start_date":"01-01-2024","end_date":"30-11-2024"}]

@router.get('/',response_model=list[Experience])
async def read_experience():
    return fake_bd
       