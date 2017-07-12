from django.contrib import admin
from chaolife.models.hotel import Hotel
from chaolife.models.image import HotelImg

class HotelImageInline(admin.StackedInline):
    model = HotelImg

class HotelInline(admin.TabularInline):
    show_change_link = True
    model = Hotel
    fields = ('name','english_name','address','introduce','contact_phone','cover_img')
    inlines = [HotelImageInline,]

class CityAdmin(admin.ModelAdmin):
    list_display = ( 'name','code','hot')
    readonly_fields = ('province',)
    inlines = [HotelInline,]
