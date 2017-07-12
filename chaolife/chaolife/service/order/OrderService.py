# -*- coding: utf-8 -*-
from chaolife.models import HotelPackageOrder, Order, Product, RoomDayState
from chaolife.serializers.orders import HotelOrderSerializer
from chaolife.tasks import notify_customer, notify_partner
from chaolife import appcodes
from common.exceptions import ConditionDenied, AdminDenied
from _datetime import datetime, timedelta
from chaolife import app_settings
from order.models import OrderBill, OrderRefund
from sms.tasks import send_order_notify_sms

"""
1.角色权限
2.订单状态
3.日期
"""


def _invalidate_can_cancel_state(hotelPackageOrder):
    """
    判断是否是合理的能够操作的用户状态
    :param user: 操作者
    :return: 返回当前的订单状态
    """
    current_process_state = hotelPackageOrder.process_state
    # 只有订单状态处于 用户发起 或者是代理商已接收的状态 才有可能执行 取消预定的操作
    if not (current_process_state == HotelPackageOrder.CUSTOMER_REQUIRE or \
                        current_process_state == HotelPackageOrder.SELLER_ACCEPT):
        raise ConditionDenied('该订单目前状态无法进行取消操作')


class HotelOrderOperationService():
    """
    HotelOrder 的一个帮助类
    涉及了 customer的取消订单，和代理商对订单的操作
    由于  customer 下订单 需要验证的逻辑更多,所以单独分离出去
    """

    def __init__(self, hotelPackageOrder, operation_user):
        self.hotelPackageOrder = hotelPackageOrder
        self.operation_user = operation_user
        self.customer = hotelPackageOrder.customer
        self.seller = hotelPackageOrder.seller
        self.cur_datetime = datetime.now()
        self.action = None
        self.orderBill = None

    def is_validate(self):
        if (self.hotelPackageOrder.closed == True):
            raise ConditionDenied('close状态下无法进行该操作')

    def cancel_book(self, commit=True):
        _invalidate_can_cancel_state(self.hotelPackageOrder)
        hotelPackageOrder = self.hotelPackageOrder

        hotelPackageOrder.state = HotelPackageOrder.CANCELED
        if self.operation_user == self.hotelPackageOrder.customer:
            self._customer_cancel()
        elif self.operation_user == self.hotelPackageOrder.seller:
            self._partner_cancel()
        if (commit):
            self.save_operation()
            # set order state has cancel

    def accept_book(self):
        # warn 这个订单的时间会不会过期，有没有做订单自动过期的功能，假设有
        # 确保当前的订单状态是可以被预订的，万一用户在这之前取消了请求呢 ?
        process_state = self.hotelPackageOrder.process_state
        if (process_state == HotelPackageOrder.CUSTOMER_REQUIRE):
            # 这是可接受预订的状态
            self.hotelPackageOrder.state = Order.PROCESSING
            self.hotelPackageOrder.process_state = HotelPackageOrder.SELLER_ACCEPT
        else:
            raise ConditionDenied('illegal opt (这个订单的状态无法执行该操作)')
        self.save_operation()

    def save_operation(self):
        self._set_modify_by()
        self.seller.save()
        self.customer.save()
        self.hotelPackageOrder.save()
        if self.orderBill:
            self.orderBill.save()
        # 积分的变化需要 创建
        # 通知用户订单变化
        extra_data = {'order': HotelOrderSerializer(self.hotelPackageOrder).data}
        self.seller.refresh_from_db()

    def _customer_cancel(self):
        # 当前订单状态 ，是否可以直接取消的操作
        # 判断当前预定的时间是否是免费的
        if self.hotelPackageOrder.process_state == HotelPackageOrder.CUSTOMER_REQUIRE:  # 如果商家未接单,全额退还
            self.hotelPackageOrder.process_state = HotelPackageOrder.CUSTOMER_CANCEL  # 标记为用户取消
            self.customer.add_customer_points(self.hotelPackageOrder.amount)
            # warn  全额退款 生成账单
        elif self.hotelPackageOrder.process_state == HotelPackageOrder.SELLER_ACCEPT:  # 商家已接单

            # warn 商家已接单
            hotelPackageOrderItems = self.hotelPackageOrder.items.select_subclasses()
            checkin_time = self.hotelPackageOrder.checkin_time

            # 入住当天6点的时间
            deduct_all_point_time = datetime(checkin_time.year, checkin_time.month, checkin_time.day,
                                             hour=18)  # 晚于这个时间扣除全部积分 (相当于默认的入住时间)

            # 入住前一天2点的时间
            dedcut_halt_point_time = deduct_all_point_time - timedelta(hours=28)  # 入住前一天的2点之后扣除一半

            self.hotelPackageOrder.process_state = HotelPackageOrder.CUSTOMER_BACK

            if self.cur_datetime < dedcut_halt_point_time:  # 未到扣除积分的时间
                self.hotelPackageOrder.process_state = HotelPackageOrder.CUSTOMER_CANCEL
                self.customer.add_customer_points(self.hotelPackageOrder.amount)
                # warn 同样的 也是i用户取消
            else:

                now = datetime.now()
                if self.cur_datetime < deduct_all_point_time:  # 扣除一半
                    need_deduct_poins = hotelPackageOrderItems[0].point * 0.5

                    if len(hotelPackageOrderItems) > 1 and now.hour >= 14:
                        need_deduct_poins += hotelPackageOrderItems[1].point * 0.5

                    need_back_to_customer_point = int(self.hotelPackageOrder.amount - need_deduct_poins)
                    orderBill = OrderBill.create_for_roomOrder_cancel(roomOrder=self.hotelPackageOrder,
                                                                      refund_amount=need_back_to_customer_point)
                    self.orderBill = orderBill
                else:  # 扣除当天全部 改代理商 %75
                    need_deduct_poins = hotelPackageOrderItems[0].point

                    if len(hotelPackageOrderItems) > 1 and now.hour >= 14:
                        need_deduct_poins += hotelPackageOrderItems[1].point * 0.5
                    need_back_to_customer_point = int(self.hotelPackageOrder.amount - need_deduct_poins)

                    orderBill = OrderBill.create_for_roomOrder_cancel(roomOrder=self.hotelPackageOrder,
                                                                      refund_amount=need_back_to_customer_point)

                    self.orderBill = orderBill
                self.hotelPackageOrder.success = True
                self.hotelPackageOrder.settled = True
        # TODO 如果
        self.hotelPackageOrder.closed = True
        self.hotelPackageOrder.success = True
        self.hotelPackageOrder.settled = True

    def _partner_cancel(self):
        # 如果是 代理商取消了订单，返回全部的积分
        process_state = self.hotelPackageOrder.process_state
        if process_state == HotelPackageOrder.SELLER_ACCEPT:
            self.hotelPackageOrder.process_state = HotelPackageOrder.SELLER_BACK
            # 代理商 在接收订单的情况下，又取消了订单，要做扣除操作
        else:  # 代理商拒绝了订单，标记为 refused
            self.hotelPackageOrder.process_state = HotelPackageOrder.SELLER_REFUSED
        self.customer.add_customer_points(self.hotelPackageOrder.total_need_points)
        self.hotelPackageOrder.closed = True
        checkin_time = self.hotelPackageOrder.checkin_time
        checkout_time = self.hotelPackageOrder.checkout_time
        RoomDayState.objects.filter(roomPackage=self.hotelPackageOrder.product, date__gte=checkin_time,
                                    date__lt=checkout_time).update(state=RoomDayState.ROOM_STATE_EMPTY)

    def _set_modify_by(self):
        # 修改订单的 modified_by 属性
        self.hotelPackageOrder.modified_by = self.operation_user

    def _is_freetime_for_cancel(self):
        if self.hotelPackageOrder.process_state == HotelPackageOrder.CUSTOMER_REQUIRE:  # 如果商家未接单
            return True
        max_later_hours = app_settings.hotelOrder_free_cancel_hours
        checkin_time = self.hotelPackageOrder.checkin_time
        checkin_time = datetime(checkin_time.year, checkin_time.month, checkin_time.day, hour=14)
        delay_date = checkin_time - timedelta(hours=max_later_hours)
        if self.cur_datetime < delay_date:  # 未到扣除积分的时间
            return True
        else:
            return False

    def _formate_opt_log(self, action, ):
        return '{user}'


def push_notify_client(hotelPackageOrder):
    """
    推送通知用户
    :param hotelPackageOrder:
    :return:
    """
    notify_template = {
        HotelPackageOrder.CUSTOMER_REQUIRE: ('下单成功,请等待处理', '您有新的订单，请注意及时及处理'),
        HotelPackageOrder.SELLER_ACCEPT: ('您的订单已被接收，请注意入住时间', '处理成功,已反馈至客户'),
        HotelPackageOrder.CUSTOMER_CANCEL: ('取消订单成功!', '请注意，您有一个订单被用户取消了'),
        HotelPackageOrder.CUSTOMER_BACK: ('取消订单成功!', '请注意，您有一个订单被用户取消了'),
        HotelPackageOrder.SELLER_REFUSED: ('很抱歉,通知您，您的订单由于代理商方原因被拒绝了', '处理成功，已反馈至客户'),
        HotelPackageOrder.SELLER_OPT_TIMEOUT: ('请注意，您有一个订单由于平台超时处理，已被自动取消', '您有一个订单，由于超时未处理已被自动取消')
    }

    template = notify_template.get(hotelPackageOrder.process_state, None)
    extra_data = {'order': HotelOrderSerializer(hotelPackageOrder).data}
    if template:
        notify_customer.delay(
            hotelPackageOrder.customer.id,
            extra_data=extra_data,
            alert=template[0]
        )

        notify_partner.delay(
            hotelPackageOrder.seller.id,
            extra_data=extra_data,
            alert=template[1]
        )


class HotelOrderProcessStateChangeHandler():
    """
    在Order save 的 signal 中，我调用了这个方法
    在订单状态已经被改变后，所做的操作。
    进行消息通知
    """

    def __init__(self, order, ):
        self._order = order

    def handle(self):
        # 加入更多可定制的通知方式
        # todo ，如果需要处理的逻辑太多，将 处理流程封装成类
        hotelPackageOrder = self._order
        push_notify_client(hotelPackageOrder)
        send_order_notify_sms.delay(hotelPackageOrder_number=hotelPackageOrder.number,
                                    process_state=hotelPackageOrder.process_state)

    def _generate_operation_text(self):
        """
        生成操作的日志
        :return:
        """
        if self._order.process_state == 1:
            pass


def check_already_refund(hotelPackageOrder):
    # if hotelPackageOrder
    return hotelPackageOrder.hotelorderoptlog_set.filter(process_state=HotelPackageOrder.REFUND_ORDER).exists()


class HotelPackageOrderStateChecker():
    @staticmethod
    def can_refund_order(hotelPackageOrder):
        if check_already_refund(hotelPackageOrder):
            raise AdminDenied('这个订单已经结算过了')


def refund_hotel_order(hotelPackageOrder):
    HotelPackageOrderStateChecker().can_refund_order(hotelPackageOrder)
    OrderRefund.create(hotelPackageOrder)
