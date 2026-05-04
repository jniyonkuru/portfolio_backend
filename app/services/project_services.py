# resources from  local packages

from app.schemas import ProjectCreate,ProjectUpdate,User
from app.repositories.base_repository import ProjectRepository
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException
from app.models import ProjectDB

async def create_project_service(project:ProjectCreate,repository:ProjectRepository,user:User)->ProjectDB |None:

     project_exists=  repository.get_by_attributes({"title":project.title,"github_url":project.github_url})
     if len(project_exists)>0:
          raise AlreadyExistException(f"Project with title :{project.title} already  exists")
     

     new_project=ProjectDB(title=project.title,description=project.description,user_id=user.id,github_url=project.github_url,tags=project.tags)
     return  repository.create(new_project)

async def get_project_by_id_service(id:int,repository:ProjectRepository)->ProjectDB |None:
     
     project= repository.get_by_id(id=id)

     if not project :
          raise  NotFoundException(f"Project with the given id :{id} was not found ")
     
     return project

async def get_list_of_project_service (repository:ProjectRepository)->list[ProjectDB]:
     return repository.get_all()

async def update_project_service(id:int,updated_project:ProjectUpdate,repository:ProjectRepository)->ProjectDB|None:
     
     project= repository.get_by_id(id)
     if not project :
          raise NotFoundException(f"project with id :{id} was not found")
     return repository.update(obj=updated_project,id=id)

async def delete_project_service(id:int,repository:ProjectRepository,user:User)->bool|None:
     
     project= repository.get_by_id(id)
     if not project:
          raise NotFoundException(f'Project with id :{id} was not found')
     return repository.delete(id)