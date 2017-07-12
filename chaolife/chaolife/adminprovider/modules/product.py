from django.contrib import admin
from django.contrib.admin import ModelAdmin
from chaolife.models.city import City
from chaolife.models.products import RoomDayState,RoomPackage


class CityInline(admin.StackedInline):
    show_change_link = True
    model = City

class ProvinceAdmin(ModelAdmin):
    list_display = ('id','name','name_py',)
    inlines = [CityInline,]

class RoomDayStateInline(admin.StackedInline):
    show_change_link = True
    model = RoomDayState
    fields = ('date','state','s_point','s_price','d_point','d_price')

def update_roomdaystate_all_enough(self,request,queryset):
    roomPackageSet = queryset.all()
    RoomDayState.objects.filter(roomPackage__in=roomPackageSet).all().update(state=RoomDayState.ROOM_STATE_ENOUGH)
    self.message_user(request,"批量修改成功")

def update_roomdaystate_all_empty(self,request,queryset):
    roomPackageSet = queryset.all()
    RoomDayState.objects.filter(roomPackage__in=roomPackageSet).all().update(state=RoomDayState.ROOM_STATE_EMPTY)
    self.message_user(request,"批量修改成功")

class RoomPackageAdmin(ModelAdmin):
    """
    酒店房型套餐
    """
    list_display = ( 'owner','hotel','room','breakfast','active','checked','deleted')
    fields = ('owner','hotel','room','breakfast','default_s_point','default_s_price','checked','active','deleted')
    list_filter = ('owner','hotel','room')
    search_fields = ('owner','hotel','rrom')
    inlines = (RoomDayStateInline,)
    actions = [update_roomdaystate_all_enough,update_roomdaystate_all_empty]

