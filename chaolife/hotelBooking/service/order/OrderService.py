from hotelBooking.models import HotelPackageOrder
from hotelBooking.serializers.orders import PartnerHotelPackageOrderSerializer, CustomerOrderSerializer
from hotelBooking.tasks import simple_notify,send_sms

class HotelOrderProcessStateChangeHandler():

    def __init__(self,order,):
        self._order = order

    def handle(self):
        # 加入更多可定制的通知方式
        # todo ，如果需要处理的逻辑太多，将 处理流程封装成类
        hotelPackageOrder = self._order
        modifyUser = hotelPackageOrder.modified_by
        if hotelPackageOrder.process_state == 1:
            pass
        elif hotelPackageOrder.process_state == 2:
            pass
        elif hotelPackageOrder.process_state == 3:
            pass
        elif hotelPackageOrder.process_state == 12:
            pass
        elif hotelPackageOrder.process_state ==13:
            pass
        c_phone_number = hotelPackageOrder.customer.phone_number
        s_phone_number = hotelPackageOrder.seller.phone_number
        print('发送通知')
        simple_notify.delay(c_phone_number,message={
        'alert': '订单操作',
        'order':CustomerOrderSerializer(hotelPackageOrder).data,
        'action':'com.pushHotel.action',
    })
        simple_notify.delay(s_phone_number,message={
        'alert': '订单操作',
        'order':PartnerHotelPackageOrderSerializer(hotelPackageOrder).data,
        'action':'com.pushHotel.action',
    } )

