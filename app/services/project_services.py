#third party packages
from fastapi import HTTPException,status
from starlette.datastructures import UploadFile

# resources from  local packages

from app.schemas import ProjectCreate,ProjectUpdate,User,Project
from app.repositories.base_repository import ProjectRepository
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException
from app.models import ProjectDB
from app.services.images_service import ImagesService


async def create_project_service(project:ProjectCreate,repository:ProjectRepository,user:User,image_service:ImagesService)->Project |None:

     github_url_exists=  repository.get_by_attributes({"github_url":project.github_url})
     if github_url_exists:
          raise AlreadyExistException(f"Project with github_url :{project.github_url} already exists")

     title_exists=  repository.get_by_attributes({"title":project.title})
     if title_exists:
          raise AlreadyExistException(f"Project with title :{project.title} already exists")

     file=await UploadFile.read(project.image)
     
     result=image_service.upload_image(file)

     if not result:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Image upload failed")
     new_project=ProjectDB(title=project.title,description=project.description,user_id=user.id,github_url=project.github_url,tags=project.tags,image=result['url'])
     project_db=repository.create(obj=new_project)
     if project_db is not None:
          return Project(id=project_db.id,created_at=project_db.created_at,updated_at=project_db.updated_at,github_url=project_db.github_url,tags=project_db.tags,image=project_db.image,description=project_db.description,title=project_db.title,user_id=project_db.user_id)
     return None
async def get_project_by_id_service(id:int,repository:ProjectRepository)->ProjectDB |None:
     
     project= repository.get_by_id(id=id)

     if not project :
          raise  NotFoundException(f"Project with the given id :{id} was not found ")
     
     return project

async def get_list_of_project_service (repository:ProjectRepository)->list[ProjectDB]:
     return repository.get_all()

async def update_project_service(id:int,updated_project:ProjectUpdate,repository:ProjectRepository,image_service:ImagesService)->ProjectDB|None:

     project= repository.get_by_id(id)
     if not project :
          raise NotFoundException(f"project with id :{id} was not found")

     github_url=getattr(updated_project,"github_url",None)
     if github_url is not None:
          github_url_owners= repository.get_by_attributes({"github_url":github_url})
          if any(existing.id != id for existing in github_url_owners):
               raise AlreadyExistException(f"Project with github_url :{github_url} already exists")

     title=getattr(updated_project,"title",None)
     if title is not None:
          title_owners= repository.get_by_attributes({"title":title})
          if any(existing.id != id for existing in title_owners):
               raise AlreadyExistException(f"Project with title :{title} already exists")

     update_payload=updated_project
     image=getattr(updated_project,"image",None)
     if image is not None:
          file=await UploadFile.read(image)
          result=image_service.upload_image(file)
          if not result:
               raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Image upload failed")
          update_payload=updated_project.model_copy(update={"image":result['url']})

     return repository.update(obj=update_payload,id=id)

async def delete_project_service(id:int,repository:ProjectRepository,user:User)->bool|None:
     
     project= repository.get_by_id(id)
     if not project:
          raise NotFoundException(f'Project with id :{id} was not found')
     return repository.delete(id)