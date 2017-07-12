from django.contrib import admin
from django.contrib.auth.models import Group
from chaolife.adminprovider.modules.product import RoomPackageAdmin
from chaolife.models import HotelPackageOrder
from chaolife.models import User,PartnerMember,CustomerMember
from chaolife.models.city import City
from chaolife.models.hotel import Hotel
from chaolife.models.image import HotelImg,RoomImg,SplashImg
from account.models import Installation
from chaolife.models.products import Product
from chaolife.models.province import Province
from chaolife.models.share import ShareNotify
from ..adminprovider.modules.city import CityAdmin
from ..adminprovider.modules.hotels import *
from ..adminprovider.modules.installation import InstallationAdmin
from ..adminprovider.modules.province import ProvinceAdmin
from ..adminprovider.modules.orders import HotelOrderAdmin

__all__ = [
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

# admin.site.register(Product,ModelAdmin)
admin.site.register(RoomPackage, RoomPackageAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(HotelPackageOrder,HotelOrderAdmin)


@admin.register(SplashImg)
class SplashImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ShareNotify)
class ShareNotifyAdmin(admin.ModelAdmin):
    pass



