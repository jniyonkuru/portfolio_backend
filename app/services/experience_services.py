
from app.repositories.base_repository import ExperienceRepository
from app.dependencies import create_experience_repo
from app.schemas.schemas import ExperienceCreate,ExperienceUpdate
from app.models.models import Experience
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException


def create_experience_service(experience:ExperienceCreate,experience_repo:ExperienceRepository):
           
                experience_exists=experience_repo.get_by_attributes({"role":experience.role,"organization":experience.organization})
                if experience_exists:
                       raise AlreadyExistException("Bad request,record already exists")
                db_experience=Experience(**experience.model_dump())
                return experience_repo.create(db_experience)
           

def get_experience_by_id_service(id:int,experience_repo:ExperienceRepository)->Experience|None:
        """"Implement service to get an experience by id"""
        experience=experience_repo.get_by_id(id)
        if not experience:
                       raise NotFoundException(f"Experience with the provided id :{id} was not found")
        return experience
        
                

def get_list_of_experiences_service(experience_repo:ExperienceRepository)->list[Experience]:
        """"Implement service to get lists of experiences"""

        return experience_repo.get_all()
       
         

def update_experience_service(experience_repo:ExperienceRepository,  update_experience:ExperienceUpdate,id:int):
                """"Implement service to update experience"""
                experience=experience_repo.get_by_id(id)
                if not experience:
                          raise NotFoundException(f'Experience with the given {id} was not found')
                return experience_repo.update(obj=update_experience,id=id)
                

def delete_experience_service(experience_repo:ExperienceRepository,id:int)->bool|None:
        """"Implement service to delete a service"""

        experience=experience_repo.get_by_id(id)
        if not experience:
                  raise NotFoundException(f'Experience with the given {id} was not found')
           
        return experience_repo.delete(id)
          
       
        



              
