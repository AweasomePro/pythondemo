from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .. import Hotel,HotelImg,House,HousePackage



class HotelLogoInline(admin.TabularInline):
    model = HotelImg

class HouseInline(admin.StackedInline):
    show_change_link = True
    model = House

class HousePackageInline(admin.StackedInline):
    show_change_link = True
    model = HousePackage
    extra = 0
    verbose_name = '套餐'
    verbose_name_plural = '套餐'

    fields = ('need_point','front_price',)

class RoomTypeAdmin(ModelAdmin):
    pass


class HotelAdmin(ModelAdmin):
    inlines = [HotelLogoInline,HouseInline]


class HotelImgAdmin(ModelAdmin):
    pass

class HouseAdmin(ModelAdmin):
    inlines = [HousePackageInline,]
    pass