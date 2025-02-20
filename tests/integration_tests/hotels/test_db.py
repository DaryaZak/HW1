from src.shemas.hotels import HotelAdd



async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Отель 5 звезд у моря", location="Сочи")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
