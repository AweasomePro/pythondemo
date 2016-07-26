from hotelBooking.models._base import BaseModel
from hotelBooking.models.user.users import User,CustomerMember,PartnerMember
from hotelBooking.models.province import Province
from hotelBooking.models.city import City
from hotelBooking.models.hotel import Hotel,Room
from hotelBooking.models.products import Product,RoomPackage,RoomDayState
from hotelBooking.models.orders import Order,OrderItem,HotelPackageOrder,HotelPackageOrderItem
from hotelBooking.models.tests import TestModel


class Meta:
    app_label = 'hotelBooking'


__all__ = [
    "BaseModel",
    "User",
    "CustomerMember","PartnerMember",
    "Province","City",
    "Hotel","Room",
    "Product","RoomPackage","RoomDayState"
]
