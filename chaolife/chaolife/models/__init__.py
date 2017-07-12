from account.models import User,CustomerMember,PartnerMember
from chaolife.models.province import Province
from chaolife.models.city import City
from chaolife.models.hotel import Hotel,Room
from chaolife.models.products import Product,RoomPackage,RoomDayState
from chaolife.models.orders import Order,OrderItem,HotelPackageOrder,HotelPackageOrderItem,HotelOrderCreditCardModel
from ..models.plugins import HotelOrderNumberGenerator
from chaolife.models.image import SplashImg
from chaolife.models.share import ShareNotify
class Meta:
    app_label = 'chaolife'


__all__ = [
    "User",
    "CustomerMember","PartnerMember",
    "Province","City",
    "Hotel","Room",
    "Product","RoomPackage","RoomDayState"
]
