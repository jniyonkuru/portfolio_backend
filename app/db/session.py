#resource form this party packages

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker,Session

#  resource from local packages
from app.db.db_config import engine


Local_session_maker=sessionmaker(bind=engine)

async_session_maker=async_sessionmaker(
    bind=engine,class_=Session,autoflush=False,autocommit=False
)

def create_session():
    with Local_session_maker() as session:
        yield session

