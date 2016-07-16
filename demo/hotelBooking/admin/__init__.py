

from django.contrib import admin
from django.contrib.auth.models import Group
from hotelBooking.adminprovider.modules.product import RoomPackageAdmin
from hotelBooking.models.city import City
from hotelBooking.models.hotel import Hotel
from hotelBooking.models.image import HotelImg,RoomImg
from hotelBooking.models.installation import Installation
from hotelBooking.models.products import Product
from hotelBooking.models.province import Province
from ..adminprovider.modules.city import CityAdmin
from ..adminprovider.modules.hotels import *
from ..adminprovider.modules.installation import InstallationAdmin
from ..adminprovider.modules.province import ProvinceAdmin

__all__ = [
    "User",
    "CustomerMember",
    "FranchiseeMember"
    "City",
    "Province",
    "Hotel",
    "Room",
    "RoomImg",
    "HotelImg",
    "Installation",
    "Order",
    "Product",
    "RoomPackage",
]



admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Installation,InstallationAdmin)
# admin.site.register(Room,RoomTypeAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(HotelImg, HotelImgAdmin)
admin.site.register(Room, RoomAdmin)

admin.site.register(Product,ModelAdmin)
admin.site.register(RoomPackage, RoomPackageAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)




