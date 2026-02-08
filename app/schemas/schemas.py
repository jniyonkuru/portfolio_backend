from sqlmodel import SQLModel, Field,Column,JSON
from pydantic import EmailStr,BaseModel
from datetime  import date,datetime
from typing import Annotated
from app.db.db_config import engine
from app.utils.pydantic_utils import make_fields_optional
from fastapi import Form,UploadFile,File

class Address(BaseModel):
    country:str
    city:str
    phone:str
#Base class for schemas and database models

# Schema base classes
class ProfileBase(SQLModel):
    email:EmailStr
    full_name:str =Field(max_length=255,min_length=20)
    image_url:str
    address:Annotated[Address,"Address of the user"]


class ProjectBase(SQLModel):
    github_url:str
    title:str =Field(index=True)
    description:str=Field(max_length=500,min_length=10,description='A text describing  the project(500 characters maximun)')
    tags:list[str]=Field(description="A list of tags")
  


class ExperienceBase(SQLModel):
    role:str =Field(max_length=255,min_length=2)
    organization:str=Field(max_length=255,min_length=2)
    start_date:date =Field(description='Starting date of the work')
    end_date:date |None =None
    tasks:list[str]=Field(description="A list of tasks carried out!")




    # Schemas for data creation
class ProfileCreate(ProfileBase):
    pass
class ProjectCreate(ProjectBase):
    pass
class ExperienceCreate(ExperienceBase):
    pass

# Schema for data updating 
ExperienceOptionalFields=make_fields_optional(model_cls=ExperienceBase,new_model_name="ExperienceUpdate")
ProjectOptionalFields=make_fields_optional(model_cls=ProjectBase,new_model_name="ProjectUpdate")
ProfileOptionalFields=make_fields_optional(model_cls=ProfileBase,new_model_name="ProfileUpdate")


class ExperienceUpdate(ExperienceOptionalFields):
    pass
class ProjectUpdate(ProjectOptionalFields):
    pass
class ProfileUpdate(ProfileOptionalFields):
    pass
