# -*- coding:utf-8 -*-
from datetime import datetime as real_datetime
from django.utils.datetime_safe import datetime
from chaolife.exceptions import ConditionDenied
import time


def caculatedaysCount(startday,endday):

    checkin_time = real_datetime.strptime(startday, '%Y-%m-%d').date()
    checkout_time = real_datetime.strptime(endday, '%Y-%m-%d').date()
    return (checkout_time - checkin_time).days

def multi_formate_str_to_date(date_str_list):
    return [formatStrToDate(date) for date in date_str_list]

def formatStrToDate(date_str):
    # todo 检查输入是否合法
    try:
        return real_datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ConditionDenied(detail='日期解析错误,正确的格式应该是 %Y-%m-%d,您的输入为{}'.format(date_str))


def today():
    """
    得到当前日期
    :return:
    """
    return datetime.today().date()