from hotelBooking.core.exceptions import ConditionDenied

class OrderDoesNotExist(ConditionDenied):
    default_detail = '不存在该订单'