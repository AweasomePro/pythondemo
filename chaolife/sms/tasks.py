from celery.task import task
from sms.client import send_notify_sms as ali_send_notify_sms
from chaolife.models import HotelPackageOrder
from sms import client as smsClient
from sms.client import send_notify_sms
from sms import config as smsConfig

@task
def send_order_notify_sms(hotelPackageOrder_number,process_state):
    print('需要查询的订单号是{}'.format(hotelPackageOrder_number))
    hotelPackageOrder = HotelPackageOrder.objects.get(number=hotelPackageOrder_number)
    notify_method_map = {
        HotelPackageOrder.CUSTOMER_REQUIRE: smsClient.notify_customer_order_create,
        HotelPackageOrder.SELLER_ACCEPT: smsClient.notify_customer_order_accepted,
        HotelPackageOrder.SELLER_REFUSED: smsClient.notify_customer_order_reject,
    }
    notify_method = notify_method_map.get(process_state, None)
    if notify_method:
        print('发送了通知')
        notify_method(hotelPackageOrder)
        if process_state == HotelPackageOrder.CUSTOMER_REQUIRE:
            smsClient.notify_admin_has_new_order(hotelPackageOrder,'')
    else:
        print('没有发送通知')


@task
def notify_customer_order_crate_success(phone_number,name,checkin_time,checkout_time,hotelname):
    send_notify_sms(phone_number, smsConfig.customer_book_hotel_code, sms_param={
        'name': name,
        'checkin_time': str(checkin_time),
        'checkout_time': str(checkout_time),
        'hotelname': hotelname,
    })

@task
def notify_reservation_update(phone_number,name,checkin_time,checkout_time,hotelname,reservation_number):
    send_notify_sms(phone_number, smsConfig.customer_book_hotel_code, sms_param={
        'name': name,
        'checkin_time': str(checkin_time),
        'checkout_time': str(checkout_time),
        'hotelname': hotelname,
        'reservation_number':reservation_number,
    })

@task
def notify_new_order(admin_phone_number,user_name,user_phone,checkin_time,checkout_time,hotel_name,partner_name,partner_phone):
    send_notify_sms(admin_phone_number,smsConfig.template_alert_new_order,sms_param={
        'user_name':user_name,
        'user_phone':user_phone,
        'checkin_time':checkin_time,
        'checkout_time':checkout_time,
        'hotelname':hotel_name,
        'partner_name':partner_name,
        'partner_phone':partner_phone,
    })