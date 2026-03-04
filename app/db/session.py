#resource form this party packages

from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker

#  resource from local packages
from app.db import engine


async_session_maker=async_sessionmaker(
    bind=engine,class_=AsyncSession,autoflush=False,autocommit=False
)
async def create_session():
   async with async_session_maker() as session:
        yield session

