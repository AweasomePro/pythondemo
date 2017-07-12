from account.models import User
from chaolife.models import HotelPackageOrder
from sms.client import send_notify_sms
from sms import config as smsConfig

def notify_customer_order_crate_success(phone_number,name,checkin_time,checkout_time,hotelname):
    send_notify_sms(phone_number, smsConfig.customer_book_hotel_code, sms_param={
        'name': name,
        'checkin_time': str(checkin_time),
        'checkout_time': str(checkout_time),
        'hotelname': hotelname,
    })

def notify_customer_order_create(order):
    phone_number = order.customer.phone_number
    print('发送短信给{}'.format(phone_number))
    hotelPacakgeOrder = order
    send_notify_sms(phone_number,smsConfig.customer_book_hotel_code,sms_param={
        'name':order.customer.name,
        'checkin_time':str(hotelPacakgeOrder.checkin_time),
        'checkout_time':str(hotelPacakgeOrder.checkout_time),
        'hotelname':hotelPacakgeOrder.hotel_name,
    })


def notify_customer_order_accepted(order):
    phone_number = order.customer.phone_number
    #warn remove ths
    hotelPacakgeOrder = order
    send_notify_sms(phone_number, smsConfig.customer_hotel_order_accept, sms_param={
        'name': order.customer.name,
        'checkin_time': str(hotelPacakgeOrder.checkin_time),
        'checkout_time':str(hotelPacakgeOrder.checkout_time),
        'hotel_name': hotelPacakgeOrder.hotel_name,
        'amount':str(hotelPacakgeOrder.total_front_prices),
    })


def notify_customer_order_reject(order):
    phone_number = order.customer.phone_number
    hotelPacakgeOrder = order
    send_notify_sms(phone_number, smsConfig.customer_hotel_order_reject, sms_param={
        'name': order.customer.name,
        'checkin_time': str(hotelPacakgeOrder.checkin_time),
        'checkout_time': str(hotelPacakgeOrder.checkout_time),
        'hotel_name': hotelPacakgeOrder.hotel_name,
        'room_name':hotelPacakgeOrder.room_name
    })


def notify_admin_has_new_order(order,admin_phone):
    user = order.customer
    seller = order.seller

    send_notify_sms(admin_phone, smsConfig.template_alert_new_order, sms_param={
        'user_name': user.name,
        'user_phone': user.phone_number,
        'checkin_time': str(order.checkin_time),
        'checkout_time': str(order.checkout_time),
        'hotelname': order.hotel_name,
        'partner_name': seller.name,
        'partner_phone': seller.phone_number,
    })
