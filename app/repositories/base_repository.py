from typing import Generic,TypeVar,Type,Any
from sqlmodel import  select,SQLModel,Session
from collections.abc import Sequence
from fastapi import Depends
from pydantic import BaseModel
from app.models.models import Experience
from abc import ABC,abstractmethod

T = TypeVar("T", bound=SQLModel)

class GenericRepository(Generic[T], ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        raise NotImplementedError
    
    @abstractmethod
    def create(self, obj: T) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, obj: T, id: int) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_attributes(self, attributes: dict[str, Any]) -> Sequence[T]:
        raise NotImplementedError


class GenericSqlRepository(GenericRepository[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.db = session

    def get_by_id(self, id: int) -> T | None:
        return self.db.get(self.model, id)
    
    def get_all(self) -> Sequence[T]:
        statement = select(self.model)
        results = self.db.exec(statement)
        return results.all()
    
    def create(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: T, id: int) -> T | None:
        item = self.get_by_id(id)
        if not item:
            return None
        
        # Convert Pydantic/SQLModel object to dict, excluding unset fields and id
        obj_data = obj.model_dump(exclude_unset=True, exclude={'id'})
        
        for key, value in obj_data.items():
            setattr(item, key, value)
        
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete(self, id: int) -> bool:
        item = self.get_by_id(id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def get_by_attributes(self, attributes: dict[str, Any]) -> Sequence[T]:
        statement = select(self.model)
        for key, value in attributes.items():
            statement = statement.where(getattr(self.model, key) == value)
        results = self.db.exec(statement)
        return results.all()


class ExperienceRepository(GenericSqlRepository[Experience]):
    def __init__(self, session: Session):
        super().__init__(Experience, session)