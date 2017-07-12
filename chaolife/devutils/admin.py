from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Apk
# Register your models here.

class ApkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Apk)