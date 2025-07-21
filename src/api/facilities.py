from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.exceptions import FacilityAlreadyExistsException, FacilityAlreadyExistsHTTPException
from src.schemas.facilities import Facility
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["facilities, Удобства"])

@router.get("/")
async def get_facilities(
        db: DBDep,
):
    return await FacilitiesService(db).get_facilities()

@router.post("/")
async def add_facility(
        db: DBDep,
        title: Facility = Body()
):
    try:
        return await FacilitiesService(db).add_facilities(title)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
