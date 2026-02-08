from fastapi import APIRouter,Body
from app.models.models import Project
from app.services.project_services import create_project_service,delete_project_service,update_project_service,get_list_of_project_service,get_project_by_id_service
from app.dependencies import ProjectRePoDeps
from app.schemas.schemas import ProjectCreate,ProjectUpdate
from typing import Annotated
router =APIRouter(
    prefix='/api/v1/projects',
    tags=["Projects"],
    responses={404:{"description":'Not found'}}
)

@router.get('/',response_model=list[Project])
async def read_projects(repository:ProjectRePoDeps):
    return get_list_of_project_service(repository=repository)

@router.post('/')
async def create_project (project:Annotated[ProjectCreate,Body()],repository:ProjectRePoDeps):
    return create_project_service(project=project,repository=repository)

@router.get('/{id}',response_model=Project)
async def get_project_by_id(id:int,repository:ProjectRePoDeps):
    return get_project_by_id_service(id=id,repository=repository)

@router.delete('/{id}')
async def delete_project(id:int,repository:ProjectRePoDeps):
    return delete_project_service(id=id,repository=repository)

@router.put('/{id}')
async def update_project(id:int ,project:ProjectUpdate,repository:ProjectRePoDeps):
    return update_project_service(id=id,updated_project=project,repository=repository)

