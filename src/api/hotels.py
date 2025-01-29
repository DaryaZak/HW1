

from fastapi import Query, Body, HTTPException, APIRouter

from src.api.dependencies import PaginationDep
from src.shemas.hotels import Hotel, HotelPatch
router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Sochi','name': 'sochi'},
    {'id': 2, 'title': 'Дубай','name': 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get('')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None,description='Айдишник'),
        title: str | None = Query(None,description='Название отеля'),

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_




@router.post('')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', "value": {
        'title': 'Отель Сочи 5 звезд у моря',
        'name': 'sochi_u_morya',
    }}})
):

    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name}
    )
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