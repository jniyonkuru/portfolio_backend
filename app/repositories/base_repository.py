#resources from  standard packages
from typing import Generic,TypeVar,Type,Any
from collections.abc import Sequence
from abc import ABC,abstractmethod

#resources from third part packages
from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError,SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

#resources from local packages

from app.models import ExperienceDB,UserDB,ProjectDB,ProfileDB
from app.utils.logger_util import  logger
from app.custom_errors.custom_errors import RepositoryError

from app.models import Base

T = TypeVar("T", bound=Base)

class GenericRepository(Generic[T], ABC):
   @abstractmethod
   async def get_by_id(self, id: int) -> T | None:
        raise NotImplementedError
    
   @abstractmethod
   async def get_all(self) -> Sequence[T]:
        raise NotImplementedError
    
   @abstractmethod
   async def create(self, obj: T) -> T:
        raise NotImplementedError
    
   @abstractmethod
   async def update(self, obj: T, id: int) -> T | None:
        raise NotImplementedError
    
   @abstractmethod
   async def delete(self, id: int) -> bool|None:
        raise NotImplementedError
    
   @abstractmethod
   async def get_by_attributes(self, attributes: dict[str, Any]) -> Sequence[T]:
        raise NotImplementedError



class GenericSqlRepository(GenericRepository[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.db = session


    async def handle_errors(self,operation:str, exception:Exception):

          logger.error(f"Repository error during {operation}:{exception}",exc_info=True,extra={"model":self.model.__name__})

          raise RepositoryError(
                  message=f'Database error during {operation}')

    async def get_by_id(self, id: int) -> T | None:
          
        try: 
            return  await self.db.get(self.model, id)
      
        except (SQLAlchemyError,DBAPIError) as e:
            await self.handle_errors(operation=f'get_by_id {id}',exception=e)
    
    async def get_all(self) -> list[T]:
        try:
            statement = select(self.model)
            results =  await self.db.execute(statement)
            return [result for result in results.scalars().all()]
        
        except (DBAPIError,SQLAlchemyError) as e:
           await  self.handle_errors(operation='get_all',exception=e)
         
    
    async def create(self, obj: T) -> T:
         try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        
         except (DBAPIError,SQLAlchemyError) as e :
             await self.db.rollback()
             await self.handle_errors(operation='create',exception=e)
          
    
    async def update(self, obj: Any, id: int) -> T | None:
        try: 
            item = await self.get_by_id(id)
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
            await self.db.commit()
            await self.db.refresh(item)
            return item
    
        except (SQLAlchemyError,DBAPIError) as e :
            await self.db.rollback()
            await self.handle_errors(operation='update',exception=e)
            
    async def delete(self, id: int) -> bool|None:
        try:
        
            item = self.get_by_id(id)
            if not item:
                return False
         
            await self.db.delete(item)
            await self.db.commit()
            return True
        except (DBAPIError,SQLAlchemyError)as  e:
            await  self.db.rollback()
            await self.handle_errors(operation='delete',exception=e)
    
    async def get_by_attributes(self, attributes: dict[str, Any]) -> list[T]:
         try:
            statement = select(self.model)
            for key, value in attributes.items():
                print(key,value)
                statement = statement.where(getattr(self.model, key) == value)
            results = await self.db.execute(statement)
            return [result for result in results.scalars().all()]
         except (DBAPIError,SQLAlchemyError)as e :
            await  self.handle_errors(operation='get_by_attributes',exception=e)
class Repo:
    def __init__(self,session:AsyncSession):
        ...


class ExperienceRepository(GenericSqlRepository[ExperienceDB],Repo):
    def __init__(self, session: AsyncSession):
        super().__init__(ExperienceDB, session) 

class ProjectRepository(GenericSqlRepository[ProjectDB],Repo):
    def __init__(self,  session: AsyncSession):
        super().__init__(ProjectDB, session)


class ProfileRepository(GenericSqlRepository[ProfileDB],Repo):
    def __init__(self,session:AsyncSession):
       super().__init__(ProfileDB,session)

class UserRepository(GenericSqlRepository[UserDB],Repo):
    def __init__(self, session:AsyncSession):
        super().__init__(UserDB, session)