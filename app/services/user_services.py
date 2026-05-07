

#resources from standard library
from typing import Any
from fastapi import HTTPException,status
from fastapi.encoders import jsonable_encoder

#resources from local packages
from app.utils.jwt_utils import decode_token
from app.utils.bcrypt_utils import generate_hash
from app.dependencies import UserRepoDeps
from app.schemas import User
from app.custom_errors import NotFoundException,AlreadyExistException
from app.schemas import UserCreate
from app.models import UserDB



class UserServices:
    def __init__(self, repository:UserRepoDeps):
        self.repository=repository
    async def current_user(self,token:str):
        payload=decode_token(token=token)
        
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        id=payload.id
        user_db= self.repository.get_by_id(id)
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        user=User(id=user_db.id,created_at=user_db.created_at,updated_at=user_db.updated_at,email=user_db.email,first_name=user_db.first_name,last_name=user_db.last_name,user_name=user_db.user_name,role=user_db.role)

        return user

    
    async def read_user_by_id(self,id:int):
        user_db =self.repository.get_by_id(id=id)
        if user_db is None:
            raise NotFoundException(message=f"User  was not found")
        
        user=User(id=user_db.id,created_at=user_db.created_at,updated_at=user_db.updated_at,email=user_db.email,first_name=user_db.first_name,last_name=user_db.last_name,user_name=user_db.user_name,role=user_db.role)

        return user 
    
    async def read_by_attributes(self,obj:dict[str,Any]):
        if len(obj)<1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request"
            )
        list_user_db= self.repository.get_by_attributes(attributes=obj)
        if len(list_user_db)<1:
            raise NotFoundException(message="User was not found")
        
        user_db=list_user_db[0]
        return user_db

    async def create_user(self,user:UserCreate):
           user_exists= self.repository.get_by_attributes({"user_name":user.user_name,"role":user.role,'email':user.email})
           if user_exists:
                raise AlreadyExistException(message="User already exists")
           hashed_passed=generate_hash(bytes(user.password,"utf-8"))
           user_db= UserDB(**user.model_dump(exclude={'password'}),password=hashed_passed)
           user_db=self.repository.create(user_db)
           return User(**jsonable_encoder(user_db))

