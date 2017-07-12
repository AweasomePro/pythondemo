from django.contrib import admin
from ..models import HotelPackageOrder
from ..models import HotelOrderOptLog

# @admin.register(HotelPackageOrder)
# class HotelPackageOderAdmin(admin.ModelAdmin):
#     pass

class OrderOptInline(admin.TabularInline):
    show_change_link = True
    model = HotelOrderOptLog

    class Meta:
        pass
