# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Feedback
# Register your models here.
@admin.register(Feedback)
class FeedBackAdmin(admin.ModelAdmin):
    pass
