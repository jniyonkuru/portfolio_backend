
#resources from standard packages 
from datetime import timedelta,datetime,timezone
import os 

#resources from third part packages
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

#resource from local packages

from app.custom_errors import CredentialException
from app.schemas import JWTPayload

load_dotenv()

secret_key=os.environ['SECRET_KEY']
access_token_expire_minutes=os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
algorithm=os.environ["ALGORITHM"]

def generate_token(payload:dict,expires_delta:timedelta |None=None):
    to_encode=payload.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+ expires_delta
    else :
        expire=datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({'exp':expire})

    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm)

    return encoded_jwt

def decode_token(token:str)->JWTPayload|None:
    try:
      payload=jwt.decode(token,secret_key,algorithms=[algorithm])
      if payload.get('id') is not None:
       return JWTPayload(id=payload['id'])
      
      return 
    except InvalidTokenError as e:
       raise CredentialException(message="Invalid token")
      