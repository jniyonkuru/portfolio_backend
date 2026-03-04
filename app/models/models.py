#Database models
from datetime  import date,datetime

# resources from  third part packages
from pydantic import EmailStr
from sqlalchemy.orm import DeclarativeBase ,mapped_column,Mapped,relationship
from sqlalchemy.types import String,Integer,DateTime,JSON
from sqlalchemy import func

# resources from local packages

from app.db import engine
from app.utils.pydantic_utils import make_fields_optional
from app.utils.utcnow import utcnow


class Base( DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__=True

    id:Mapped[int]=mapped_column()
    created_at:Mapped[datetime]=mapped_column(DateTime,default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=func.now(),onupdate=func.now())
    

class Address():
    country:str
    city:str
    phone:str
#Base class for schemas and database models

# Schema base classes
class ProfileDB(Base):
    __tablename__="profiles"

    user_id:Mapped[int]=mapped_column(Integer,unique=True,nullable=False,index=True,foreign_key="userdb.id")
    image_url:Mapped[str]=mapped_column(String(255))
    address:Mapped[Address]=mapped_column(JSON)
    users=relationship("UserDB",back_populates="profile")


class ProjectDB(Base):
    __tablename__= "projects"
    github_url:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    title:Mapped[str]=mapped_column(String(255),nullable=False)
    description:Mapped
    tags:Mapped[list[str]]=mapped_column(JSON)
    user_id:Mapped[int]=mapped_column(Integer,foreign_key="userdb.id")
    users=relationship("UserDB",back_populates="projects")
  

class ExperienceDB(Base):
    __tablename__="experiences"
    role:Mapped[str]=mapped_column(String(255),nullable=False)
    organization:Mapped[str]=mapped_column(String(255),nullable=False)
    start_date:Mapped[date]=mapped_column(DateTime,nullable=False)
    end_date:Mapped[date]=mapped_column(DateTime,nullable=True)
    tasks:Mapped[list[str]]=mapped_column(JSON)
    user_id:Mapped[int]=mapped_column(Integer,foreign_key="userdb.id")
    users=relationship("UserDB",back_populates="projects")


class UserDB(Base):
    __tablename__  =""
    first_name:Mapped[str]=mapped_column(String(255),nullable=False)
    last_name:Mapped[str]=mapped_column(String(255),nullable=False)
    email:Mapped[EmailStr]=mapped_column(String(255),unique=True,nullable=False,index=True)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    projects=relationship("ProjectDB",back_populates="users")
    profile=relationship("ProfileDB",back_populates="users",uselist=False)