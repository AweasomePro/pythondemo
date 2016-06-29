from django.contrib import admin

from hotelBooking import Hotel

class HotelInline(admin.TabularInline):
    show_change_link = True
    model = Hotel

class CityAdmin(admin.ModelAdmin):
    list_display = ('name_py', 'name','logo', 'province')
    inlines = [HotelInline,]
