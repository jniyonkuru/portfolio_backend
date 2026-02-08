from fastapi import HTTPException,FastAPI,Request
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import experiences,projects
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.db.db_config import create_db_and_tables
from app.custom_errors.custom_errors import AlreadyExistException,NotFoundException,RepositoryError
from  fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.logger_util import logger

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator:
 try:
  create_db_and_tables()
  logger.info("Database initialized successfully")
  yield
 except Exception as e:
  logger.error(f"Failed to initialize database:{e}")
  raise
 finally:
  logger.info("Application shutting down")

app=FastAPI(lifespan=lifespan,title="Portfolio API",description="API for my porfolio")

@app.exception_handler(NotFoundException)
async def not_found_handler(request:Request,exc:NotFoundException):
   return JSONResponse(
    status_code=404,
    content={"message":exc.message}
   )

@app.exception_handler(AlreadyExistException)
async def already_exists_handler(request:Request,exc:AlreadyExistException):
 return JSONResponse(
  status_code=409,
  content={"message":exc.message}
 )

@app.exception_handler(RepositoryError)
async def repository_exception_handler(request:Request,exc:RepositoryError):
 return JSONResponse(
  status_code=500,
  content={"message":f"Internal server exception occured:{exc}"}
 )


app.include_router(experiences.router)
app.include_router(projects.router)