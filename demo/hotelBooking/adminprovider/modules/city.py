from django.contrib import admin
from hotelBooking.models.hotel import Hotel


class HotelInline(admin.TabularInline):
    show_change_link = True
    model = Hotel

class CityAdmin(admin.ModelAdmin):
    list_display = ( 'name','code', 'province')
    inlines = [HotelInline,]
