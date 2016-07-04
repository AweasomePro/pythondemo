from hotelBooking.models import User
from .core.models.city import City
from .core.models.province import Province
from .core.models.hotel import Hotel,House
from .core.models.image import HotelImg,HouseImg
from .core.models.installation import Installation
from .core.models.user import CustomerMember,FranchiseeMember
from .core.models.orders import Order,HotelPackageOrder,HotelPackageOrderSnapShot
from .core.models.products import Product,HousePackage
from .core.models.plugins import HotelOrderNumberGenerator
import signal


__all__ = [
    "User",
    "CustomerMember",
    "FranchiseeMember"
    "City",
    "Province",
    "Hotel",
    "House",
    "HouseImg",
    "HotelImg",
    "Installation",
    "Order",
    "Product",
    "HousePackage",

]