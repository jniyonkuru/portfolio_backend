from fastapi import APIRouter
from pydantic import BaseModel
router =APIRouter(
    prefix='/projects',
    tags=["Projects"],
    responses={404:{"description":'Not found'}}
)
class Project(BaseModel):
    id:str
    title:str
    images:list[str]
    description:str
# read a  list of projects
@router.get('/',response_model=list[Project])
async def read_projects():
    pass


