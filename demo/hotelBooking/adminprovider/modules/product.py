from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .. import City

class CityInline(admin.StackedInline):
    show_change_link = True
    model = City

class ProvinceAdmin(ModelAdmin):
    list_display = ('id','name','name_py',)
    inlines = [CityInline,]

class HousePackageAdmin(ModelAdmin):
    """
    酒店房型套餐
    """
    list_display = ( 'owner','house','breakfast','need_point','front_price','active','checked','detail')
    fields = ('owner','house','breakfast','need_point','front_price','checked','active','detail')
    readonly_fields = ()