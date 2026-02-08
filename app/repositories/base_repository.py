from typing import Generic,TypeVar,Type,Any
from sqlmodel import  select,SQLModel,Session
from collections.abc import Sequence
from fastapi import Depends
from pydantic import ValidationError
from app.models.models import Experience,Project,Profile
from app.schemas.schemas import ExperienceUpdate
from abc import ABC,abstractmethod
from app.utils.logger_util import  logger
from app.custom_errors.custom_errors import RepositoryError
from sqlalchemy.exc import DBAPIError,SQLAlchemyError

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
    def delete(self, id: int) -> bool|None:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_attributes(self, attributes: dict[str, Any]) -> Sequence[T]:
        raise NotImplementedError



class GenericSqlRepository(GenericRepository[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.db = session


    def handle_errors(self,operation:str, exception:Exception):

          logger.error(f"Repository error during {operation}:{exception}",exc_info=True,extra={"model":self.model.__name__})

          raise RepositoryError(
                  message=f'Database error during {operation}')

    def get_by_id(self, id: int) -> T | None:
          
        try: 
            return self.db.get(self.model, id)
      
        except (SQLAlchemyError,DBAPIError) as e:
            self.handle_errors(operation=f'get_by_id {id}',exception=e)
    
    def get_all(self) -> list[T]:
        try:
            statement = select(self.model)
            results = self.db.exec(statement)
            return list(results.all())
        
        except (DBAPIError,SQLAlchemyError) as e:
            self.handle_errors(operation='get_all',exception=e)
         
    
    def create(self, obj: T) -> T:
         try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        
         except (DBAPIError,SQLAlchemyError) as e :
             self.db.rollback()
             self.handle_errors(operation='create',exception=e)
          
    
    def update(self, obj: Any, id: int) -> T | None:
        try: 
            item = self.get_by_id(id)
            if not item:
                    return None
            if hasattr(obj,"model_dump"):
            # Convert Pydantic/object to dict, excluding unset fields and id
               obj_data = obj.model_dump(exclude_unset=True, exclude={'id'})
            else:
                obj_data =obj.dict(exclude_unset=True,exclude={'id'})

            for key, value in obj_data.items():
                setattr(item, key, value)
            
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
    
        except (SQLAlchemyError,DBAPIError) as e :
            self.db.rollback()
            self.handle_errors(operation='update',exception=e)
            
    def delete(self, id: int) -> bool|None:
        try:
        
            item = self.get_by_id(id)
            if not item:
                return False
         
            self.db.delete(item)
            self.db.commit()
            return True
        except (DBAPIError,SQLAlchemyError)as  e:
            self.db.rollback()
            self.handle_errors(operation='delete',exception=e)
    
    def get_by_attributes(self, attributes: dict[str, Any]) -> list[T]:
         try:
            statement = select(self.model)
            for key, value in attributes.items():
                print(key,value)
                statement = statement.where(getattr(self.model, key) == value)
            results = self.db.exec(statement)
            return list(results.all())
         except (DBAPIError,SQLAlchemyError)as e :
             self.handle_errors(operation='get_by_attributes',exception=e)
class Repo:
    def __init__(self,session:Session):
        ...


class ExperienceRepository(GenericSqlRepository[Experience],Repo):
    def __init__(self, session: Session):
        super().__init__(Experience, session) 

class ProjectRepository(GenericSqlRepository[Project],Repo):
    def __init__(self,  session: Session):
        super().__init__(Project, session)


class ProfileRepository(GenericSqlRepository[Profile],Repo):
    def __init__(self,session:Session):
       super().__init__(Profile,session)