
#resources from standard packages 
from typing import Annotated
import os
from datetime import timedelta
#resources from third part packages 
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv

# resources from local packages 

from app.schemas import User,Credentials,UserRoles
from app.dependencies import oauth2_scheme
from app.services.user_services import UserServices
from app.utils.jwt_utils import decode_token,generate_token
from app.utils.bcrypt_utils import verify_password
from app.custom_errors import NotFoundException



load_dotenv()
access_token_minutes=os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
router=APIRouter(
    prefix='/api/v1/users',
    tags=['users']
)

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],user_services:Annotated[UserServices,Depends(UserServices)]):
          payload=decode_token(token=token)
          if payload is None:
                 raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token")
          user=await user_services.read_user_by_id(id=payload.id)

          return user

def require_role(roles:list[UserRoles]):
       async def role_checker(user:Annotated[User,Depends(get_current_user)]):
              if user.role not in roles:
                     raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient permission"
                     )
              return  user
    
       return  role_checker

     
async def login(credentials:Credentials,user_services:Annotated[UserServices,Depends(UserServices)]):
    try:
       user= await user_services.read_by_attributes({'user_name':credentials.username})

       if user is None:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password')
       
       password_match=verify_password(password=bytes(credentials.password,'utf-8'),hashed_password=user.password)
    
       if not password_match:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password ')
       access_token_expires=timedelta(minutes=float(access_token_minutes))
       token = generate_token(payload={"id":1},expires_delta=access_token_expires)

       return {
              "token_type":"bearer ",
              "access_token":token
           }

    except NotFoundException :
          raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect user name or password"
          )

@router.get('/me',response_model=User)
async def current_user(user:Annotated[User,Depends(get_current_user)]): 
    return user

@router.post('/token')
async def user_login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],user_services:Annotated[UserServices,Depends(UserServices)]):
      credentials=Credentials(username=form_data.username,password=form_data.password)
      token =await login(credentials=credentials,user_services=user_services)
      return token
