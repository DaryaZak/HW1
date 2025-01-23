

from fastapi import FastAPI, Query, Body, HTTPException
#from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi','name': 'sochi'},
    {'id': 2, 'title': 'Дубай','name': 'dubai'}
]

@app.get('/hotels')
def get_hotels(
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
    return hotels_

@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': 'Sochi'}
    )
    return {'status': 'OK'}

@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

@app.put('/hotels/{hotel_id}')
def update_hotel(hotel_id: int, update_data: dict = Body(...)):
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


@app.patch('/hotels/{hotel_id}')
def update_hotel(hotel_id: int, update_data: dict = Body(...)):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if 'title' in update_data:
                hotel['title'] = update_data['title']
            if 'name' in update_data:
                hotel['name'] = update_data['name']
            return {"message": "Hotel updated", "hotel": hotel}

    raise HTTPException(status_code=404, detail="Hotel not found")

#@app.get(path:'/docs', include_in_schema=False)
#async def


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
