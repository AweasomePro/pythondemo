from django.contrib.admin import ModelAdmin


class InstallationAdmin(ModelAdmin):
    list_display = ('deviceToken',)