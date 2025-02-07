

from fastapi import Query, Body, APIRouter
from src.api.dependencies import PaginationDep, DBDep

from src.shemas.hotels import Hotel, HotelPatch, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])



@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None,description='локация'),
        title: str | None = Query(None,description='Название отеля'),

):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get('/{hotel_id}')
async def get_hotel(hotel_id:int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)




@router.post('')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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

    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'OK', 'data': hotel}



@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}



@router.put('/{hotel_id}')
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}')
async def update_hotel_part(hotel_id: int, hotel_data: HotelPatch, db: DBDep,):

    await db.hotels.edit(hotel_data,exclude_unset = True, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}

