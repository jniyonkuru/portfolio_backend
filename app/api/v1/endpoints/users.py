
#resources from standard packages 
from typing import Annotated
#resources from third part packages 
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm

# resources from local packages 

from app.schemas import User,Credentials
from app.dependencies import oauth2_scheme
from app.services.user_services import UserServices

router=APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)


@router.get('/me',response_model=User)
async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],user_service:Annotated[UserServices,Depends(UserServices)]): 
    user= await user_service.current_user(token=token)
    return user

@router.post('/token')
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],user_service:Annotated[UserServices,Depends(UserServices)]):
      credentials=Credentials(username=form_data.username,password=form_data.password)
      token =await user_service.login(credentials=credentials)

      return token
