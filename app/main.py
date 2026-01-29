from fastapi import HTTPException,FastAPI,Request
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import experiences
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.db.db_config import create_db_and_tables
import logging


logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

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

app.include_router(experiences.router)