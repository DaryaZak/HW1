from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException
from src.api.dependencies import PaginationDep, DBDep
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.services.hotels import HotelService
from src.shemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2025-02-11"),
    date_to: date = Query(example="2025-02-11"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "name": "sochi_u_morya",
                    "location": " Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель У фонтана",
                    "name": "dubai_fountain",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).update_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_hotel_part(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
):
    await HotelService(db).update_hotel_part(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}
