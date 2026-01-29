#Database models
from sqlmodel import Field,Column,JSON
from ..schemas.schemas import ProfileBase,ProjectBase,ExperienceBase,Address


class Project(ProjectBase, table=True):
    id: int|None =Field(default=None,primary_key=True)
    

class Experience(ExperienceBase,table=True):
    id:int|None=Field(default=None,primary_key=True)
    tasks:list[str]=Field(sa_column=Column(JSON))
    

class Profile(ProfileBase,table=True):
    id:int|None =Field(default=None,primary_key=True)
    address:Address=Field(sa_column=Column(JSON))


print(type(Experience))