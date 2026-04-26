#Database models
from datetime  import date,datetime

# resources from  third part packages
from pydantic import EmailStr,AnyUrl
from sqlalchemy.orm import DeclarativeBase ,mapped_column,Mapped,relationship
from sqlalchemy.types import String,Integer,DateTime,JSON,LargeBinary
from sqlalchemy import func,ForeignKey,Enum

# resources from local packages

from app.utils.pydantic_utils import make_fields_optional
from app.utils.utcnow import utcnow
from  app.schemas import UserRoles


class Base( DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__=True

    id:Mapped[int]=mapped_column(primary_key=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=func.now(),onupdate=func.now())
    

class Address():
    country:str
    city:str
    phone:str
#Base class for schemas and database models

# Schema base classes
class ProfileDB(BaseModel):
    __tablename__="profiles"

    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("users.id"),unique=True,nullable=False,index=True,)
    image_url:Mapped[str]=mapped_column(String(255))
    address:Mapped[Address]=mapped_column(JSON)
    users=relationship("UserDB",back_populates="profile")


class ProjectDB(BaseModel):
    __tablename__= "projects"

    github_url:Mapped[str]=mapped_column(String(255),unique=True,nullable=False)
    title:Mapped[str]=mapped_column(String(255),nullable=False)
    description:Mapped[str]=mapped_column(String(255),nullable=False)
    tags:Mapped[list[str]]=mapped_column(JSON)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("users.id"))
    users=relationship("UserDB",back_populates="projects")
  

class ExperienceDB(BaseModel):
    __tablename__="experiences"

    role:Mapped[str]=mapped_column(String(255),nullable=False)
    organization:Mapped[str]=mapped_column(String(255),nullable=False)
    start_date:Mapped[date]=mapped_column(DateTime,nullable=False)
    end_date:Mapped[date]=mapped_column(DateTime,nullable=True)
    tasks:Mapped[list[str]]=mapped_column(JSON)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey("users.id"))
    users=relationship("UserDB",back_populates="experiences")


class UserDB(BaseModel):
    __tablename__  ="users"
    
    first_name:Mapped[str]=mapped_column(String(255),nullable=False)
    last_name:Mapped[str]=mapped_column(String(255),nullable=False)
    user_name:Mapped[str]=mapped_column(String(255),nullable=False, index=True,unique=True)
    email:Mapped[EmailStr]=mapped_column(String(255),unique=True,nullable=False,index=True)
    role:Mapped[UserRoles]=mapped_column(String(255),Enum(UserRoles),nullable=False)
    password:Mapped[bytes]=mapped_column(LargeBinary,nullable=False)
    projects=relationship("ProjectDB",back_populates="users")
    profile=relationship("ProfileDB",back_populates="users",uselist=False)
    experiences=relationship("ExperienceDB",back_populates="users")