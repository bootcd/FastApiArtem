from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility

router = APIRouter(prefix="/facilities", tags=["facilities, Удобства"])

@router.get("/")
async def get_facilities(
        db: DBDep,
):
    facilities = await db.facilities.get_all()
    return {"status": "ok", "data": facilities}

@router.post("/")
async def add_facility(
        db: DBDep,
        title: Facility = Body()
):
    try:
        facility = await db.facilities.add(data=title)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    else:
        await db.commit()

    return {"status": "ok", "data": facility}