from fastapi import HTTPException,FastAPI,Request
from fastapi.responses import JSONResponse
from api.v1.endpoints import experiences
app=FastAPI()
app.include_router(experiences.router)