from django.contrib.auth.models import Group
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from hotelBooking.adminprovider.modules.product import HousePackageAdmin
from .. import Province,City,Hotel,House,HouseImg, HotelImg,HousePackage,User,CustomerMember,PartnerMember,Installation,Product
from ..models import User
from ..adminprovider.modules.user import UserAdmin, UserChangeForm, UserCreationForm, MyUserAdmin
from ..adminprovider.modules.province import ProvinceAdmin
from ..adminprovider.modules.city import CityAdmin
from ..adminprovider.modules.installation import InstallationAdmin
from ..adminprovider.modules.hotels import *

from ..models import User
from ..core.models.city import City
from ..core.models.province import Province
from ..core.models.hotel import Hotel,House
from ..core.models.image import HotelImg,HouseImg
from ..core.models.installation import Installation
from ..core.models.user import CustomerMember,PartnerMember
from ..core.models.orders import Order
from ..core.models.products import Product,HousePackage
import signal
from django.contrib import admin

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



admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Installation,InstallationAdmin)
# admin.site.register(RoomType,RoomTypeAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(HotelImg, HotelImgAdmin)
admin.site.register(House,HouseAdmin)

admin.site.register(Product,ModelAdmin)
admin.site.register(HousePackage,HousePackageAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)




