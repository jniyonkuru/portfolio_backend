from sqlmodel import SQLModel, Field
from pydantic import PastDate,EmailStr
from typing import TypedDict
from app.db.db_config import engine

class Address(TypedDict):
    country:str
    city:str
    phone:str
#Base class for schemas and database models

# Schema base classes
class ProfileBase(SQLModel):
    email:EmailStr
    full_name:str =Field(max_length=255,min_length=20)
    image_url:str
    address:Address


class ProjectBase(SQLModel):
    mage_url:str
    title:str =Field(index=True)
    description:str=Field(max_length=500,min_length=10,description='A text describing  the project(500 characters maximun)')


class ExperienceBase(SQLModel):
    role:str =Field(max_length=255,min_length=2)
    organization:str=Field(max_length=255,min_length=2)
    start_date:PastDate =Field(description='Starting date of the work')
    end_date:PastDate |None =None
    tasks:list[str]


#Database models

class ProjectDB(ProjectBase, table=True):
    id: int|None =Field(default=None,primary_key=True)
    

class ExperienceDB(ExperienceBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    

class ProfileDB (ProfileBase,table=True):
    id:int|None =Field(default=None,primary_key=True)


    # Schema for data creation
class ProfileCreate(ProfileBase):
    pass
class ProjectCreate(ProjectBase):
    pass
class ExperienceCreate(ExperienceBase):
    pass

