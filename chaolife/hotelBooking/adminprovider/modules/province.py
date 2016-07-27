from django.contrib import admin
from django.contrib.admin import ModelAdmin
from hotelBooking.models.city import City


class CityInline(admin.StackedInline):
    show_change_link = True
    model = City

class ProvinceAdmin(ModelAdmin):
    list_display = ('id','name',)
    inlines = [CityInline,]