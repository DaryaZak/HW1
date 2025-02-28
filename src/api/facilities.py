from fastapi import Body, APIRouter
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.shemas.facilities import FacilityAdd
from src.api.dependencies import DBDep



router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
