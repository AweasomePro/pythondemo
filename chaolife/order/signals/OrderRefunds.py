from django.db.models import signals
from django.dispatch import receiver,Signal
from ..models import OrderRefund,OrderBill
from common.utils.logger import normal_logger
from chaolife.models.orders import HotelPackageOrder
will_gains_points = Signal(providing_args=['player','points','src_model'])

@receiver(signals.post_save,sender =OrderRefund)
def on_orderRefund_post_save(instance,created,update_fields,**kwargs):
    if created:
        normal_logger.warn(msg='有管理员为订单创建了退单')

    orderRefund = instance
    order = orderRefund.order
    hotelPackageOrder = order.hotelpackageorder
    tracker = orderRefund.tracker
    print('order refund saved')
    # warn changed 是上次的值
    print(tracker.changed())

    # 根据 order Refund 状态 相应改变 HotelPackageOrder的状态
    if tracker.has_changed('state'):
        if orderRefund.state == OrderRefund.STATE_REJECT:
            #拒绝赔付，目前该情况不存在
            pass
        elif orderRefund.state == OrderRefund.STATE_ACCEPT:
            hotelPackageOrder.process_state = HotelPackageOrder.REFUND_ORDER_PART_SUCCESS
            hotelPackageOrder.save(update_fields=('process_state',))
            pass
        elif orderRefund.state == OrderRefund.STATE_REFUND_PARTIAL:
            hotelPackageOrder.tag_refund_partial_success()
            pass
        elif orderRefund.state == OrderRefund.STATE_SUCCESS:
            # 赔付完成,未该订单生成 订单结算
            hotelPackageOrder.tag_refund_success()
            OrderBill.create_for_refund_order(orderRefund)
            pass
