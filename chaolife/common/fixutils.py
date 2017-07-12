from chaolife.models import RoomPackage,Order,HotelPackageOrder
from account.models import Installation
from django.db import transaction
def fix_roomPackageName():
    roomPackages_ite = RoomPackage.objects.prefetch_related('hotel','room').iterator()
    with transaction.atomic():
        for roomPackage in roomPackages_ite:
            roomPackage.hotel_name = roomPackage.hotel.name
            roomPackage.room_name = roomPackage.room.name
            roomPackage.checked = True
            roomPackage.deleted = False
            roomPackage.active = True
            roomPackage.save()


def fix_product_city():
    roomPackages_ite = RoomPackage.objects.prefetch_related('hotel', 'room').iterator()
    with transaction.atomic():
        for roomPackage in roomPackages_ite:
            roomPackage.city = roomPackage.hotel.city
            roomPackage.save()

def fix_order_data():
    HotelPackageOrder.objects.all().filter(success=True).update(closed=True,status = Order.COMPLETE)
    HotelPackageOrder.objects.all().\
        filter(process_state__in = (HotelPackageOrder.CUSTOMER_CANCEL,
                                    HotelPackageOrder.SELLER_OPT_TIMEOUT,
                                    HotelPackageOrder.CUSTOMER_BACK,
                                    HotelPackageOrder.SELLER_REFUSED,
                                    HotelPackageOrder.SELLER_BACK,
                                    HotelPackageOrder.OVER_CHECKOUT_TIME))\
        .update(closed=True,status = Order.CANCELED)
    HotelPackageOrder.objects.all().filter(process_state=HotelPackageOrder.PERFECT_SELL,).update(closed=True,success=True,settled=True)

def fix_installtion_channels():
    Installation.objects.prefetch_related('user').filter(user__role=2).update(channels=['Hpartner'])
    Installation.objects.prefetch_related('user').filter(user__role=1).update(channels=['customer'])
