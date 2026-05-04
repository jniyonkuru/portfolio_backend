#resources from standard packages 
from typing import Annotated

#resources from third part packages
from fastapi import APIRouter,Body,Depends

#resources from  local packages
from app.services.project_services import create_project_service,delete_project_service,update_project_service,get_list_of_project_service,get_project_by_id_service
from app.dependencies import ProjectRePoDeps
from app.schemas import Project,ProjectCreate,ProjectUpdate,UserRoles,User
from app.api.v1.endpoints.users import require_role

router =APIRouter(
    prefix='/api/v1/projects',
    tags=["Projects"],
    responses={404:{"description":'Not found'}}
)

@router.get('/',response_model=list[Project])
async def read_projects(repository:ProjectRePoDeps):
    return await get_list_of_project_service(repository=repository)

@router.post('/')
async def create_project (project:Annotated[ProjectCreate,Body()],repository:ProjectRePoDeps,user:Annotated[User,Depends(require_role(roles=[UserRoles.ADMIN]))]):
    return await create_project_service(project=project,repository=repository,user=user)

@router.get('/{id}',response_model=Project)
async def get_project_by_id(id:int,repository:ProjectRePoDeps):
    return await get_project_by_id_service(id=id,repository=repository)

@router.delete('/{id}')
async def delete_project(id:int,repository:ProjectRePoDeps,user:Annotated[User,Depends(require_role(roles=[UserRoles.ADMIN]))]):
    return await delete_project_service(id=id,repository=repository,user=user)

@router.put('/{id}')
async def update_project(id:int ,project:ProjectUpdate,repository:ProjectRePoDeps, user:Annotated[User,Depends(require_role([UserRoles.ADMIN]))]):
    return await update_project_service(id=id,updated_project=project,repository=repository)

