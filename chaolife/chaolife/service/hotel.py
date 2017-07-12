from django.db.models import Prefetch
from django.db.models import Min
from chaolife.models.products import RoomDayState,RoomPackage
from django.core import cache
from chaolife.cache import generate_hotel_min_price_cache_key
from ..serializers.products import RoomDayStateSerializer


def get_hotel_min_price(hotel,startdate):
    #获得某个酒店下当天最低的价格
    default_cache = cache.get_cache('default')
    cache_key = generate_hotel_min_price_cache_key(hotel,startdate)
    cache_value = default_cache.get(generate_hotel_min_price_cache_key(hotel,startdate), )
    if cache_value:
        return cache_value
    # 没有缓存，读取数据库
    roomDaystate = RoomDayState.objects.filter(hotel=hotel, date=startdate). \
        select_related('roomPackage','room').filter(roomPackage__active=True,room__active=True).order_by('s_price','s_point').first()
    min_price_json = RoomDayStateSerializer(roomDaystate, exclude_fields=('id','state')).data
    default_cache.set(cache_key, min_price_json, 600)
    return min_price_json
