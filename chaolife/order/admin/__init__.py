from django.contrib import admin
from django.contrib.admin import ModelAdmin
# from .hotelpackageorders import HotelPackageOderAdmin
from ..models import HotelPackageOrder,OrderRefund,OrderBill
from django import forms
from django.contrib import messages




@admin.register(OrderRefund)
class OrderRefundAdmin(ModelAdmin):
    readonly_fields =('order','product','seller','proposer')
    pass

@admin.register(OrderBill)
class OrderBillAdmin(ModelAdmin):
    readonly_fields = ('order','seller',)