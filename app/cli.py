import uvicorn
import asyncio
from app.user_seed import seed_user

def dev():
    uvicorn.run(
        "app.main:app",
        reload=True,
        port=8002,
        host='127.0.0.1',

    )

def prod():
    uvicorn.run(
        "app.main:app",
        host='0.0.0.0',
        reload=True,
        port=8000
    )

   