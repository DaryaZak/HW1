from datetime import date

from fastapi import Query, Body, APIRouter

from src.exceptions import RoomNotFoundHTTPException, HotelNotFoundHTTPException, RoomNotFoundException, \
    HotelNotFoundException
from src.services.rooms import RoomService
from src.shemas.rooms import RoomAddRequest, RoomPatchRequest

from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-02-11"),
    date_to: date = Query(example="2025-02-11"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep
):
    await RoomService(db).update_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_hotel_part(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    await RoomService(db).update_hotel_part(hotel_id, room_id, room_data)
    return {"status": "OK"}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)

    return {"status": "OK"}
