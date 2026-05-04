#resources from standard packages
import os
import json
import asyncio

#resources from third part  packages

from sqlalchemy.orm import Session
from sqlalchemy import select
import typer
from dotenv import load_dotenv

#resources from local packages 
from app.models.models import UserDB
from app.utils.logger_util import logger
from app.db.session import create_session
from app.utils.bcrypt_utils import generate_hash

load_dotenv()

password=os.environ["PASSWORD"]

app=typer.Typer()

def create_user_seed(session:Session):
   
    json_path=os.path.join(
        os.path.dirname(__file__),"user.json"
    )
    try:
      with open(json_path,'r') as file:
        user=json.load(file)

      result= session.execute(select(UserDB).where(UserDB.email==user["email"]))
      user_exists=result.scalar_one_or_none()

      if  user_exists:
       logger.info("User with the given email already exists")
       return 
      
      hashed_password=generate_hash(bytes(password,'utf-8'))
      user.update({"password":hashed_password})

      new_user=UserDB(**user)

      session.add(new_user)
      session.commit()
      session.refresh(new_user)
      logger.info("User seeded successfully!")
 
    except FileNotFoundError:
        session.rollback()
        logger.error(f"userjson file was not found on path: {json_path}")
    
    except json.JSONDecodeError:
       session.rollback()
       logger.error("Invalid json format .")
    
    except Exception as e:
       session.rollback()
       logger.info(f"Error while seeding user:{e}")
    

@app.command()
def seed_user():
  """seed user from user.json file"""
  def run_seed():
     for session in create_session():
           create_user_seed(session=session)

  run_seed()


if __name__=="__main__":
   app()