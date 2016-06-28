
import datetime
from django.utils.encoding import force_text
def get_unique_reference_number(order):
    now = datetime.datetime.now()
    dt = "%012s%07d%04d" % (now.strftime("%y%m%d%H%M%S"), now.microsecond * 1000000, 10 % 1000)
    return dt + calc_reference_number_checksum(dt)


def calc_reference_number_checksum(rn):
    """
    计算 引用编号,输出一个数字，这个数字可以用来检验
    :param rn: 源编号
    :return: 输出
    """
    muls = (7, 3, 1)
    s = 0
    for i, ch in enumerate(rn[::-1]):
        s += muls[i % 3] * int(ch)
    s = 10 - (s % 10)
    return force_text(s)[-1]

def get_unique_reference_number(order):
    now = datetime.now()


print(calc_reference_number_checksum('10002'))