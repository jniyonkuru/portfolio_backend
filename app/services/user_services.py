

#resources from standard library
import os
from datetime import timedelta
from typing import Any
#resources from third part packages
from fastapi import HTTPException,status
from dotenv import load_dotenv

#resources from local packages 
from app.repositories import UserRepository
from app.utils.jwt_utils import generate_token, decode_token
from app.utils.bcrypt_utils import verify_password
from app.dependencies import UserRepoDeps
from app.schemas import User
from app.custom_errors import NotFoundException


class UserServices:
    def __init__(self, repository:UserRepoDeps):
        self.repository=repository
    async def current_user(self,token:str):
        payload=decode_token(token=token)
        
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        id=payload.id
        userDB= self.repository.get_by_id(id)
        if userDB is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        user=User(id=userDB.id,created_at=userDB.created_at,updated_at=userDB.updated_at,email=userDB.email,first_name=userDB.first_name,last_name=userDB.last_name,user_name=userDB.user_name,role=userDB.role)

        return user
        
    # async def login(self,credentials:Credentials):
          
    #       if not credentials:
    #           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Incorrect username or password ")
          
    #       result= await self.repository.get_by_attributes({'user_name':credentials.username})
          
    #       if len(result) < 1:
    #           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password')
    #       user =result[0]

    #       password_match=verify_password(password=bytes(credentials.password,'utf-8'),hashed_password=user.password)
    
    #       if not password_match:
    #           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password ')
    #       access_token_expires=timedelta(minutes=float(access_token_minutes))
    #       token = generate_token(payload={"id":1},expires_delta=access_token_expires)

    #       return {
    #           "token_type":"bearer ",
    #           "access_token":token
    #       }
    
    async def read_user_by_id(self,id:int):

        userDB =self.repository.get_by_id(id=id)

        if userDB is None:
            raise NotFoundException(message=f"User  was not found")
        
        user=User(id=userDB.id,created_at=userDB.created_at,updated_at=userDB.updated_at,email=userDB.email,first_name=userDB.first_name,last_name=userDB.last_name,user_name=userDB.user_name,role=userDB.role)

        return user 
    
    async def read_by_attributes(self,obj:dict[str,Any]):
        if len(obj)<1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request"
            )
        print("########################++++++#######################")
        print(obj)

        list_userDB= self.repository.get_by_attributes(attributes=obj)
        print("########################++++++#######################")
        if len(list_userDB)<1:
            raise NotFoundException(message="User was not found")
        
        userDB=list_userDB[0]
        return userDB