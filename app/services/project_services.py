from app.schemas.schemas import ProjectCreate,ProjectUpdate
from app.repositories.base_repository import ProjectRepository
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException
from app.models.models import Project

def create_project_service(project:ProjectCreate,repository:ProjectRepository)->Project |None:

     project_exists=repository.get_by_attributes({"title":project.title,"github_url":project.github_url})
     if(x:=len(project_exists)>0):
          raise AlreadyExistException(f"Project with title :{project.title} already  exists")
     new_project=Project(**project.model_dump())
     return repository.create(new_project)

def get_project_by_id_service(id:int,repository:ProjectRepository)->Project |None:
     
     project=repository.get_by_id(id=id)

     if not project :
          raise  NotFoundException(f"Project with the given id :{id} was not found ")
     
     return project

def get_list_of_project_service (repository:ProjectRepository)->list[Project]:
     
     return repository.get_all()

def update_project_service(id:int,updated_project:ProjectUpdate,repository:ProjectRepository)->Project|None:
     
     project=repository.get_by_id(id)
     if not project :
          raise NotFoundException(f"project with id :{id} was not found")
     return repository.update(obj=updated_project,id=id)

def delete_project_service(id:int,repository:ProjectRepository)->bool|None:
     
     project=repository.get_by_id(id)
     if not project:
          raise NotFoundException(f'Project with id :{id} was not found')
     return repository.delete(id)