#resources from standard packages
import os
import json
import asyncio

#resources from third part  packages
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import typer

#resources from local packages 
from app.models.models import UserDB
from app.utils.logger_util import logger
from app.db.session import create_session



app=typer.Typer()
async def create_user_seed(session:AsyncSession):
   
    json_path=os.path.join(
        os.path.dirname(__file__),"user.json"
    )
    try:

      with open(json_path,'r') as file:
        user=json.load(file)

      result= await session.execute(select(UserDB).where(UserDB.email==user["email"]))
      user_exists=result.scalar_one_or_none()

      if  user_exists:
       logger.info("User with the given email already exists")
       return 
    
      new_user=UserDB(first_name=user["first_name"],last_name=user["last_name"],email=user['email'],user_name=user['user_name'],password=user['password'])
      session.add(new_user)
      await session.commit()
      await session.refresh(new_user)
      logger.info("User seeded successfully!")
 
    except FileNotFoundError:
      await session.rollback()
      logger.error(f"userjson file was not found on path: {json_path}")
    
    except json.JSONDecodeError:
       await session.rollback()
       logger.error("Invalid json format .")
    
    except Exception as e:
       await session.rollback()
       logger.info(f"Error while seeding user:{e}")
    



@app.command()
def seed_user():
  """seed user from user.json file"""
  async def run_seed():
   async for session in create_session():
      await create_user_seed(session=session)
  asyncio.run(run_seed())


if __name__=="__main__":
   app()