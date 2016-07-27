from django.contrib import admin
from django.contrib.admin import ModelAdmin
from hotelBooking.models.city import City


class CityInline(admin.StackedInline):
    show_change_link = True
    model = City

class ProvinceAdmin(ModelAdmin):
    list_display = ('id','name','name_py',)
    inlines = [CityInline,]

class RoomPackageAdmin(ModelAdmin):
    """
    酒店房型套餐
    """
    list_display = ( 'owner','room','breakfast','default_s_point','default_s_price','active','checked',)
    fields = ('owner','room','breakfast','default_s_point','default_s_price','checked','active',)
    readonly_fields = ()