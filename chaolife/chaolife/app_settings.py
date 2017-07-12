# -*- coding:utf-8 -*-
from chaolifeProject.settings import TEST
from datetime import timedelta
point_tax = 0.75  # 对卖家所获得积分的费率 如100积分的交易，卖家只能获得 75积分
point_delay_automatic_account_hours = 24  # 成功的交易，何时积分才会自动到达卖家的账号
hotelOrder_free_cancel_hours = 24 # 消费者免费取消预定的时间
min_front_price = 100 # 最低房费
custom_cancel_hours = timedelta(hours=2)
point_price = 10 # 1块钱所能换算的积分
point_flow_to_seller_hours =  24
if TEST: #如果是测试服，重载掉某些参数
    from .debug_settings import *