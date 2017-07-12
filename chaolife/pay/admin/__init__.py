from django.contrib import admin
from ..models import PointPay,Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'state','reject_reason')


@admin.register(PointPay)
class PointPayAdmin(admin.ModelAdmin):
    list_display = ('user','trade_no','unit_price','number','total_price')
    fields = ('user','trade_no','number','total_price','unit_price','pay_method','status')
    readonly_fields = ('user','trade_no','pay_method','status')
