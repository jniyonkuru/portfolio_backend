
#resources from standards packages

from contextlib import asynccontextmanager
from typing import AsyncGenerator

#resources from  third part packages
from  fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException,FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

#resources from local  packages
from app.utils.logger_util import logger
from app.db.db_config import create_db_and_tables
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException,RepositoryError,CredentialException
from app.api.v1.endpoints import experiences,projects,profiles,users


@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator:
 try:
  await create_db_and_tables()
  logger.info("Database initialized successfully")
  yield
 except Exception as e:
  logger.error(f"Failed to initialize database:{e}")
  raise
 finally:
  logger.info("Application shutting down")

app=FastAPI(title="Portfolio API",lifespan=lifespan,description="API for my porfolio")
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.exception_handler(NotFoundException)
async def not_found_handler(request:Request,exc:NotFoundException):
   return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"message":exc.message}
   )

@app.exception_handler(AlreadyExistException)
async def already_exists_handler(request:Request,exc:AlreadyExistException):
 return JSONResponse(
  status_code=status.HTTP_409_CONFLICT,
  content={"message":exc.message}
 )

@app.exception_handler(RepositoryError)
async def repository_exception_handler(request:Request,exc:RepositoryError):
 return JSONResponse(
  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
  content={"message":f"Internal server exception occured:{exc}"}
 )
@app.exception_handler(CredentialException)
async def credential_exception_handler(reques:Request,exc:CredentialException):
 return JSONResponse(
  status_code=status.HTTP_400_BAD_REQUEST,
  content={
   "message":exc.message
  }
 )

app.include_router(experiences.router)
app.include_router(projects.router)
app.include_router(profiles.router)
app.include_router(users.router)




