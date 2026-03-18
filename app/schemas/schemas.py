# resources from standard packages
from datetime import datetime
from typing_extensions import Self

#resources from third part packages 
from pydantic import BaseModel,Field,AnyUrl,EmailStr,model_validator

#resources from local packages
from app.utils.pydantic_utils import make_fields_optional

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
    github_url:AnyUrl=Field(max_length=255, description="title of the project")
    title:str=Field(max_length=255,description="Title of the project")
    tags:list[str]=Field(description="A list of tags")


class UserBase(BaseModel):
    first_name:str=Field(max_length=255,description="User's first Name")
    last_name:str=Field(max_length=255,description="User's last Name")
    user_name:str=Field(max_length=255,description="user_name")
    email:EmailStr=Field(description="User's email")



class ExperienceBase(BaseModel):
    role:str=Field(max_length=255, description="Roles Undertakend")
    organization:str=Field(max_length=255,description="Organization name")
    start_date:datetime=Field(description="Starting date")
    end_date:datetime=Field(description="End date")
    tasks:list[str]=Field(description='a list of tasks undertaken',default=[])

    @model_validator(mode='after')
    def validates_date(self)->Self:
        if self.start_date>=self.end_date:
            raise ValueError("Starting date  can not be after the ending date")
        return self


class ProfileBase(BaseModel):
    image_url:AnyUrl|None=Field(max_length=255, description="Profile picture url", default=None)
    address:Address=Field(description="User's address")



class ProfileCreate(ProfileBase):
    user_id:int|None=Field(description="User's id", default=None)

class ProjectCreate(ProjectBase):
    user_id:int|None=Field(description="User's id", default=None)
class ExperienceCreate(ExperienceBase):
    user_id:int|None=Field(description="User's id", default=None)

class UserCreate(UserBase):
    password:str=Field(description="Password")


class Profile(ProfileCreate,Base):
    pass

class Project(ProjectCreate,Base):
    pass

class Experience(ExperienceCreate,Base):
    pass

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