#resources from local packages
from app.repositories.base_repository import ExperienceRepository
from app.schemas import ExperienceCreate,ExperienceUpdate,User
from app.models import ExperienceDB
from app.custom_errors import AlreadyExistException,NotFoundException


async def create_experience_service(experience:ExperienceCreate,experience_repo:ExperienceRepository,user:User):
           
                experience_exists= await experience_repo.get_by_attributes({"role":experience.role,"organization":experience.organization})
                if (x:=len(experience_exists)>0):
                       raise AlreadyExistException("Bad request,record already exists")
                db_experience=ExperienceDB(role=experience.role,
                         organization=experience.organization,
                         start_date=experience.start_date,
                         end_date=experience.end_date,
                         tasks=experience.tasks,
                         user_id=user.id)
                
                return  await experience_repo.create(db_experience)
           

async def get_experience_by_id_service(id:int,experience_repo:ExperienceRepository)->ExperienceDB|None:
        """"Implement service to get an experience by id"""
        experience= await experience_repo.get_by_id(id)
        if not experience:
                       raise NotFoundException(f"Experience with the provided id :{id} was not found")
        return experience
        
                

async def get_list_of_experiences_service(experience_repo:ExperienceRepository)->list[ExperienceDB]:
        """"Implement service to get lists of experiences"""

        return await experience_repo.get_all()
       
         

async def update_experience_service(experience_repo:ExperienceRepository,  update_experience:ExperienceUpdate,id:int):
                """"Implement service to update experience"""
                experience=await experience_repo.get_by_id(id)
                if not experience:
                          raise NotFoundException(f'Experience with the given {id} was not found')
                return await experience_repo.update(obj=update_experience,id=id)
                

async def delete_experience_service(experience_repo:ExperienceRepository,id:int)->bool|None:
        """"Implement service to delete a service"""

        experience= await experience_repo.get_by_id(id)
        if not experience:
                  raise NotFoundException(f'Experience with the given {id} was not found')
           
        return await experience_repo.delete(id)

          
       
        



              
