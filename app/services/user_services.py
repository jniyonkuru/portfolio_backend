

#resources from standard library
from typing import Any
from fastapi import HTTPException,status

#resources from local packages
from app.utils.jwt_utils import decode_token
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
        list_userDB= self.repository.get_by_attributes(attributes=obj)
        if len(list_userDB)<1:
            raise NotFoundException(message="User was not found")
        
        userDB=list_userDB[0]
        return userDB