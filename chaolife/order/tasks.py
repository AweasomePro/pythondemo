# encoding:utf-8
from datetime import timedelta, datetime
from django.db import transaction
from django.db.models import Q,F,Prefetch
from chaolifeProject.celery import app
from celery.utils.log import get_task_logger
from chaolife.models.orders import HotelPackageOrder,Order
from chaolife.serializers.orders import HotelOrderSerializer

from chaolife.tasks import notify_partner,notify_customer
from order.models import OrderBill
logger = get_task_logger(__name__)

@app.task(bind = True,)
def check_expired_order(self,):
    #检查过期的交易，
    # 商家超时未确认的,将它关闭，并退还用户积分
    now = datetime.now()
    with transaction.atomic():
        #todo 用pretch_related 提高性能 slect_for_update 所匹配的行会被锁定，直到 事物结束
        all_need_closed_order = HotelPackageOrder.objects.select_for_update().filter(closed=False,process_state=1).all()
        for hotelPackageOrder in all_need_closed_order.iterator():
            with transaction.atomic():
                bookTime = hotelPackageOrder.created
                # 预订的时间
                book_hour = bookTime.hour
                should_cancel = False
                if ((book_hour>=0 and book_hour<9) and now.day == bookTime.day) or ((book_hour>21) and now.day > bookTime.day):
                    print('now book_hour type is {}'.format(now.hour))
                    if now.hour >= 11:
                        should_cancel = True
                elif (book_hour>=9 and book_hour <=19) and (now.hour - bookTime.hour)>2:
                    should_cancel = True
                elif (book_hour>=19 and book_hour <21) and now.day > bookTime.day and now.hour>8:
                    should_cancel = True
                if should_cancel:
                    hotelPackageOrder.tag_opt_tiemout()
    return 'task is success'


@app.task(bind = True)
def check_should_checkin_order(self,):
    """
    检查订单状态是 双方正常交易，并且入住时间已过的。将 process_state 修改为100.
    :param self:
    :return:
    """
    now = datetime.now() - timedelta(hours=18) #默认入住时间是下午两点，但是到达六点时是无法取消订单的而由于数据库中保存的是date
    with transaction.atomic(): #直接就表示用户　入住　success.
        hotelPackageOrderSet = HotelPackageOrder.objects.\
            filter(Q(process_state=HotelPackageOrder.SELLER_ACCEPT) & Q(checkin_time__lte=now))
        for hotelPackageOrder in hotelPackageOrderSet.iterator():
            customer = hotelPackageOrder.customer
            notify_customer(customer.id,extra_data={'order':HotelOrderSerializer(hotelPackageOrder).data},alert='入住时间快到了,请注意')

@app.task(bind = True)
def check_should_tag_checkin_order(self,):
    """
    检查订单状态是 双方正常交易，并且入住时间已过的。将 process_state 修改为100.
    :param self:
    :return:
    """
    now = datetime.now() - timedelta(hours=24) #在当日24点 标记为 checkin时间，
    with transaction.atomic(): #直接就表示用户　入住　success.
        hotelPackageOrderSet = HotelPackageOrder.objects.select_for_update().\
            filter(Q(process_state=HotelPackageOrder.SELLER_ACCEPT) & Q(checkin_time__lte=now))
        for hotelPackageOrder in hotelPackageOrderSet.iterator():
            hotelPackageOrder.process_state = HotelPackageOrder.ARRIVE_CHECK_IN_TIME
            hotelPackageOrder.save()


@app.task(bind=True)
def check_should_tag_checkout_order(self,):
    #检查订单状态是 arriva_checkin 而且当前时间已经过了checkout的,
    now = datetime.now()-timedelta(hours=12)
    with transaction.atomic():
        will_settled_order = HotelPackageOrder.objects.select_for_update().filter(
            process_state=HotelPackageOrder.ARRIVE_CHECK_IN_TIME,checkout_time__lte=now,
        ).all().iterator()
        for hotelPackageOrder in will_settled_order:
            try:
                hotelPackageOrder.orderbill
                #warn 已经存在结算单，不应该存在这个情况，可能是后台误操作
            except OrderBill.DoesNotExist:
                hotelPackageOrder.tag_already_checkout()
                orderBill = OrderBill.create_for_perfect_room_sell(hotelPackageOrder)
                orderBill.save()
            pass
                #warn errror


@app.task(bind = True)
def order_point_to_seller_account(self,):
    #todo 订单完成 交易成功，并且时间超过2天的积分要到账
    now = datetime.now()  # 默认 积分到达代理商段的时间是 checkout 2天以后，为了测试，我将时间改为14,因为默认checkout time 是14点
    with transaction.atomic():  # 直接就表示用户　入住　success. warn ARRIVE_CHECK_IN_TIME 该成 ARRIVE_CHECKOUT_TIME
        for orderBill in OrderBill.objects.filter(settled=False,delay_settlement_time__lt=now).prefetch_related('seller',).iterator():
            will_gains_points =  orderBill.seller_gains
            orderBill.settled = True
            orderBill.save()
            order = orderBill.order
            order.settled = True
            hotelPackageOrder = HotelPackageOrder.objects.select_for_update().get(number=order.number)
            hotelPackageOrder.process_state = HotelPackageOrder.PERFECT_SELL
            hotelPackageOrder.status = Order.COMPLETE
            hotelPackageOrder.save()
            orderBill.seller.add_partner_points(will_gains_points)
            from chaolife.serializers import HotelOrderSerializer
            notify_partner.delay(user_id=orderBill.seller_id ,extra_data = HotelOrderSerializer(hotelPackageOrder).data,alert='订单结算通知',)
