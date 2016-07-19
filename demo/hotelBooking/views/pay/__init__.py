from hotelBooking.module.alipay import Alipay
from .config import settings
alipay2 = Alipay(
    pid= settings.ALIPAY_PARTNER ,
    key=settings.ALIPAY_KEY,
    seller_email= settings.ALIPAY_SELLER_EMAIL
)