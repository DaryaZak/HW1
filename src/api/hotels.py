

from fastapi import Query, Body, HTTPException, APIRouter
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels', tags=['Отели'])



@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None,description='Айдишник'),
        title: str | None = Query(None,description='Название отеля'),

):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )



        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


    #if pagination.page and pagination.per_page:
        #return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]





@router.post('')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 звезд у моря",
            "name": "sochi_u_morya",
            "location": " Сочи, ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель У фонтана",
            "name": "dubai_fountain",
            "location": "Дубай, ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()


    return {'status': 'OK'}

@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

@router.put('/{hotel_id}')
def update_hotel(hotel_id: int, hotel_data: Hotel, update_data: dict = Body(...)):
    if len(update_data) == 1:
        raise HTTPException(
            status_code=400,
            detail="Both 'title' and 'name' must be provided together"
        )

    if len(update_data) == 0:
        raise HTTPException(
            status_code=400,
            detail="Request body cannot be empty"
        )

    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel.update(update_data)
            return {"message": "Hotel updated", "hotel": hotel}

    raise HTTPException(status_code=404, detail="Hotel not found")


@router.patch('/{hotel_id}')
def update_hotel_part(hotel_id: int, hotel_data: HotelPatch, update_data: dict = Body(...)):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if 'title' in update_data:
                hotel['title'] = update_data['title']
            if 'name' in update_data:
                hotel['name'] = update_data['name']
            return {"message": "Hotel updated", "hotel": hotel}

    raise HTTPException(status_code=404, detail="Hotel not found")

