#-*- coding: utf-8 -*-
"""
将所有的业务逻辑封装到service模块中
最小化model 和 view ,
多数情况下，Service对象的方法应该是无状态的，即它们基于函数参数不使用任何的类属性来独立执行动作
所以，我们最好将它们明确的标记为静态方法

"""
from .order.OrderService import HotelOrderOperationService