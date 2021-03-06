from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ValidationError

from chaolife.models.hotel import Room
from chaolife.models.image import HotelImg
from chaolife.models.products import RoomPackage
from ...models import Hotel
from django.contrib import messages

class HotelLogoInline(admin.TabularInline):
    model = HotelImg

class RoomInline(admin.StackedInline):
    show_change_link = True
    model = Room

class RoomPackageInline(admin.StackedInline):
    show_change_link = True
    model = RoomPackage
    verbose_name = '套餐'
    verbose_name_plural = '套餐'
    extra = 0
    fields = ('default_s_point','default_s_price','breakfast','owner','detail','checked','active','room')


class HotelAdmin(ModelAdmin):
    inlines = [HotelLogoInline, RoomInline]
    list_display = ('name','city')
    list_filter = ('name','city__name')
    search_fields = ['name','city__name']


class HotelImgAdmin(ModelAdmin):
    pass


class RoomAdmin(ModelAdmin):
    list_display = ('hotel', 'name','checked','active',)
    fields = ('hotel', 'name', 'checked', 'active')
    search_fields = ('hotel__name','active')

