from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_edit = False
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Bookings):
    column_list = [
        Bookings.id,
        Bookings.user_id,
        Bookings.room_id,
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
    ]
    can_delete = True
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-address-book"


class HotelAdmin(ModelView, model=Hotels):
    column_list = [Hotels.id, Hotels.name, Hotels.location]
    can_delete = True
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Rooms):
    column_list = [Rooms.id, Rooms.hotel_id, Rooms.description, Rooms.price]
    can_delete = True
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"
