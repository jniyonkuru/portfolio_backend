from typing import Annotated

from fastapi import APIRouter,Body,Depends

from app.services.profile_services import create_profile_service,edit_profile_service,get_a_list_of_profiles_service,delete_profile_service,get_profile_by_id_service
from app.dependencies import  ProfileRepoDeps
from app.schemas import Profile,ProfileCreate,ProfileUpdate,User,UserRoles
from app.api.v1.endpoints.users import require_role

router=APIRouter(prefix="/api/v1/profiles",
                 tags=["Profiles"],
                 responses={404:{"description":"Not found"}}
                 )

@router.post('/',response_model=Profile)
async def create_profile(profile:Annotated[ProfileCreate,Body()],repository:ProfileRepoDeps,user:Annotated[User,Depends(require_role(roles=[UserRoles.ADMIN]))]):
    return await  create_profile_service(profile=profile,repository=repository,user=user)

@router.get('/',response_model=list[Profile])
async def get_a_list_profiles(repository:ProfileRepoDeps):
    return  await get_a_list_of_profiles_service(repository=repository)

@router.get('/{id}',response_model=Profile)
async def get_profile_by_id(id:int,repository:ProfileRepoDeps):
    return await  get_profile_by_id_service(id=id, repository=repository)

@router.put('/{id}',response_model=Profile)
async def update_profile(id:int,profile:Annotated[ProfileUpdate,Body()],repository:ProfileRepoDeps,user:Annotated[User,Depends(require_role(roles=[UserRoles.ADMIN]))]):
    return await edit_profile_service(id=id,profile_update=profile,repository=repository,user=user)

@router.delete('/{id}')
async def delete_profile(id:int,repository:ProfileRepoDeps,user:Annotated[User,Depends(require_role(roles=[UserRoles.ADMIN]))]):
    return await  delete_profile_service(id=id,repository=repository)
