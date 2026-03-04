# resources from third part packages
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

#resources form standard packages
import os

# resources from local packages
from app.models import Base

load_dotenv()

DATABASE_URL=os.environ["DATABASE_URL"]
engine = create_async_engine(DATABASE_URL, echo=True)

    #create  database tables
async def create_db_and_tables():
    async with engine.begin() as conn:
     await conn.run_sync( Base.metadata.create_all)

