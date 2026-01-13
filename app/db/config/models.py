from base_class import Base
from sqlmodel import Field
from pydantic import PastDate,EmailStr
from typing import TypedDict


class Address(TypedDict):
    country:str
    city:str
    phone:str

class ProjectDBase(Base):
    id: int|None =Field(default=None,primary_key=True)
    image_url:str
    title:str =Field(index=True)
    description:str=Field(max_length=500,min_length=10,description='A text describing  the project(500 characters maximun)')

class ExperienceDB(Base):
    id:int|None=Field(default=None,primary_key=True)
    role:str =Field(max_length=255,min_length=2)
    organization:str=Field(max_length=255,min_length=2)
    start_date:PastDate =Field(description='Starting date of the work')
    end_date:PastDate |None =None
    tasks:list[str]

class Profile (Base):

    id:int|None =Field(default=None,primary_key=True)
    email:EmailStr
    full_name:str =Field(max_length=255,min_length=20)
    image_url:str
    address:Address
