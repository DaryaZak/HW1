from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.shemas.bookings import Booking
from src.shemas.facilities import Facility
from src.shemas.hotels import Hotel
from src.shemas.rooms import Room
from src.shemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking

class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility