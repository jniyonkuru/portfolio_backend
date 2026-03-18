

#resources from standard library
import os
from datetime import timedelta
#resourcces from third part packages 
from fastapi import HTTPException,status
from dotenv import load_dotenv

#resources from local packages 
from app.repositories import UserRepository
from app.utils.jwt_utils import generate_token, decode_token
from app.utils.bcrypt_utils import verify_password
from app.dependencies import UserRepoDeps
from app.schemas import Credentials,User


load_dotenv()
access_token_minutes=os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
class UserServices:
    def __init__(self, repository:UserRepoDeps):
        self.repository=repository
    async def current_user(self,token:str):
        payload=decode_token(token=token)
        
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        id=payload.id
        userDB= await self.repository.get_by_id(id)
        if userDB is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not login !")
        
        user=User(id=userDB.id,created_at=userDB.created_at,updated_at=userDB.updated_at,email=userDB.email,first_name=userDB.first_name,last_name=userDB.last_name,user_name=userDB.user_name)

        return user
        
    async def login(self,credentials:Credentials):
          
          if not credentials:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Incorrect username or password ")
          
          result= await self.repository.get_by_attributes({'user_name':credentials.username})
          
          if len(result) < 1:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password')
          user =result[0]

          password_match=verify_password(password=bytes(credentials.password,'utf-8'),hashed_password=user.password)
          print(f"password match:{password_match}")
          if not password_match:
              raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect username or password ')
          access_token_expires=timedelta(minutes=float(access_token_minutes))
          token = generate_token(payload={"id":1},expires_delta=access_token_expires)

          return {
              "token_type":"bearer ",
              "access_token":token
          }

     