from typing import Generic,TypeVar
from sqlmodel import  select,SQLModel,Session
from collections.abc import Sequence
from fastapi import Depends
T=TypeVar("T",bound=SQLModel)
 
class BaseRepository(Generic[T]):
    def __init__(self,model:type[T],session:Session):
        self.model=model
        self.db=session

    def get_by_id(self,id:int)->T |None:
        return self.db.get(self.model,id)
    
    def get_all(self,limit:int=10,skip:int=0)->Sequence[T]:
        statement=select(self.model).limit(limit).offset(skip)
        results=self.db.exec(statement)
        return results.all()
    
    def create (self,obj:T)->T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update (self,obj:T,id:int):
        item=self.get_by_id(id)
        if not item:
            return None
        obj_data=obj.model_dump(exclude_unset=True ,exclude={'id'})
        
        for key,value in obj_data.items():
            setattr(item,key,value)
    
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete(self,id:int):
        item=self.get_by_id(id)
        if not item :
            return False
        self.db.delete(item)
        self.db.commit()
    def get_by_attribute(self,attributes:dict[str,str])->Sequence[T]:
        statement=select(self.model)
        for key in attributes.keys():
            statement=statement.where(self.model[key]==attributes[key])
        

        results=self.db.exec(statement)
        return results.all()
   