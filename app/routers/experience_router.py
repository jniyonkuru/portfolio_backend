from fastapi import APIRouter

router = APIRouter(
    prefix="/experiences",
    tags=["experiences"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_experiences():
    await  get_experiences()
