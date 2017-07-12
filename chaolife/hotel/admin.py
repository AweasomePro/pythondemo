# -*- coding:utf-8 -*-
from django.contrib import admin
# Register your models here.
from .models import HotelType
@admin.register(HotelType)
class HotelTypeAdmin(admin.ModelAdmin):
    pass
