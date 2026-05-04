from app.schemas.schemas import ProfileCreate,ProfileUpdate
from app.repositories.base_repository import ProfileRepository
from app.custom_errors.custom_errors import NotFoundException ,AlreadyExistException
from app.models import ProfileDB

async def create_profile_service(profile:ProfileCreate,repository:ProfileRepository):
      
          profile_exist= repository.get_by_attributes({"user_id":profile.user_id})

          if profile_exist:
                  raise AlreadyExistException(message="Profile already exists")
          new_profile=ProfileDB(**profile.model_dump())
          return   repository.create(new_profile)

async def edit_profile_service(id:int,profile_update:ProfileUpdate,repository:ProfileRepository):
        
        profile= repository.get_by_id(id=id)
        if not profile :
                raise NotFoundException(message=f"Profile with id :{id} was not found")
         
        return repository.update(obj=profile_update,id=id)

async def get_profile_by_id_service(id:int,repository:ProfileRepository):
        
        profile= repository.get_by_id(id=id)

        if not profile :
                raise NotFoundException(message="Profile with id:{id} was not found!")
        
        return profile

async def get_a_list_of_profiles_service(repository:ProfileRepository):
        
        return  repository.get_all()
async def  delete_profile_service(id:int,repository:ProfileRepository):
        
        profile=  repository.get_by_id(id=id)

        if not profile :
                raise NotFoundException(message="profile with id :{id} was not found")
        
        return  repository.delete(id=id)