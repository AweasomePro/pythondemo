from django.contrib import admin
from order.admin.hotelpackageorders import OrderOptInline
class HotelOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('number','customer','seller','product','hotel_name','amount','total_front_prices')
    fields = (
            'number',
            ('seller','customer'),
            'hotel_name','amount',
            'total_front_prices',
            ('checkin_time','checkout_time'),
            'status',
            'process_state')
    inlines = [OrderOptInline,]