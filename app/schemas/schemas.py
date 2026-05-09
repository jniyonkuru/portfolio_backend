# resources from standard packages
from datetime import datetime
from typing_extensions import Self
from enum import Enum

#resources from third part packages 
from pydantic import BaseModel,Field,AnyUrl,EmailStr,model_validator
from fastapi import UploadFile
#resources from local packages
from app.utils.pydantic_utils import make_fields_optional
#user roles

class UserRoles(str,Enum):
    ADMIN='admin'

class Address(BaseModel):
    country:str
    city:str
    phone:str

class JWTPayload(BaseModel):
    id:int
class Credentials(BaseModel):
    username:str
    password:str

class Base(BaseModel):
    id:int
    created_at:datetime
    updated_at:datetime

class ProjectBase(BaseModel):
    github_url:str=Field(max_length=255, description="title of the project")
    description:str=Field(max_length=500,description="A text description the Project")
    title:str=Field(max_length=255,description="Title of the project")
    tags:list[str]=Field(description="A list of tags")


class UserBase(BaseModel):
    first_name:str=Field(max_length=255,description="User's first Name")
    last_name:str=Field(max_length=255,description="User's last Name")
    user_name:str=Field(max_length=255,description="user_name")
    email:EmailStr=Field(description="User's email")
    role:UserRoles=Field(description="User's role")


class ExperienceBase(BaseModel):
    role:str=Field(max_length=255, description="Roles Undertaken")
    organization:str=Field(max_length=255,description="Organization name")
    start_date:datetime=Field(description="Starting date")
    end_date:datetime|None=Field(description="End date",default=None)
    tasks:list[str]=Field(description='a list of tasks undertaken',default=[])

    @model_validator(mode='after')
    def validates_date(self)->Self:
        if self.end_date and self.start_date>=self.end_date:
            raise ValueError("Starting date  can not be after the ending date")
        return self


class ProfileBase(BaseModel):
    image_url:AnyUrl|None=Field(max_length=255, description="Profile picture url", default=None)
    address:Address=Field(description="User's address")



class ProfileCreate(ProfileBase):
    pass

class ProjectCreate(ProjectBase):
    image: UploadFile = Field(description="Project ui image if any")

class ExperienceCreate(ExperienceBase):
   pass

class UserCreate(UserBase):
    password:str=Field(description="Password")


class Profile(ProfileBase,Base):
    user_id: int = Field(description="User's id")

class Project(ProjectCreate,Base):
    user_id: int = Field(description="User's id")
    image :str=Field(description="Project image")

class Experience(ExperienceCreate,Base):
    user_id: int = Field(description="User's id")

class User(UserBase,Base):
    pass



# Schema for data updating 
ExperienceOptionalFields=make_fields_optional(model_cls=ExperienceCreate,new_model_name="ExperienceUpdate")
ProjectOptionalFields=make_fields_optional(model_cls=ProjectCreate,new_model_name="ProjectUpdate")
ProfileOptionalFields=make_fields_optional(model_cls=ProfileCreate,new_model_name="ProfileUpdate")
UserOptionalFields=make_fields_optional(model_cls=UserCreate,new_model_name="UserUpdate")


class ExperienceUpdate(ExperienceOptionalFields):
    pass
class ProjectUpdate(ProjectOptionalFields):
    pass
class ProfileUpdate(ProfileOptionalFields):
    pass
class UserUpdate(UserOptionalFields):
    pass