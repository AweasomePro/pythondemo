from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import Province,City,Hotel,House,HouseImg, HotelImg,HousePackage,User,CustomerMember,PartnerMember,Installation,Product
from .models import User
from .adminprovider.modules.user import UserAdmin, UserChangeForm, UserCreationForm, MyUserAdmin
from .adminprovider.modules.province import ProvinceAdmin
from .adminprovider.modules.city import CityAdmin
from .adminprovider.modules.installation import InstallationAdmin
from .adminprovider.modules.hotels import *



# Now register the new UserAdmin...
admin.site.register(User, MyUserAdmin)
admin.site.register(CustomerMember,ModelAdmin)
admin.site.register(PartnerMember, ModelAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Installation,InstallationAdmin)
# admin.site.register(RoomType,RoomTypeAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(HotelImg, HotelImgAdmin)
admin.site.register(House,HouseAdmin)

admin.site.register(HousePackage,ModelAdmin)
admin.site.register(Product,ModelAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)



# Register your models here

