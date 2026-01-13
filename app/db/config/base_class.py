from sqlmodel import SQLModel

class Base(SQLModel,table=True):
    pass