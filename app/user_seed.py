from app.db.db_config import engine
from app.models.models import UserDB
from sqlmodel import Session,select
from app.utils.logger_util import logger
import os
import json
from app.db.session import async_session_maker

def seed_user(session:Session):

   try: 
    json_path=os.path.join(
        os.path.dirname(__file__),"user.json"
    )
    with open(json_path,'r') as file:
        user=json.load(file)

    user_exists=session.exec(select(UserDB).where(UserDB.email==user["email"]))

    print("user",user['first_name'])
    
    if  user_exists is not None:
       new_user=UserDB(first_name=user["first_name"],last_name=user["last_name"],email=user['email'],password=user['password'])
       session.add(new_user)
       session.commit()
       session.refresh(new_user)
       logger.info("User seeded successfully!")
    

   except Exception as e:
      session.rollback()
      logger.info("Error while seeding user")


async def run_seed(func):
     async with async_session_maker()as session:
         func(session)