import random
from datetime import datetime

from django import forms
from django.db import models
from django.db import transaction
productTypeMap = {
    "hotelPackage":"01"
}

"""
订单号规则:
年后2位+月份+日期+当天订单数量+商品类型+随机数
"""

class OrderNumberGenerator(models.Model):
    id = models.CharField(primary_key=True,max_length=20)

    class Meta:
        app_label = 'chaolife'
        abstract = True

    def init(self,request,order=None):
        self.request = request
        self.order = order

    def exclude_form_fields(self):
        """
        Returns a list of fields, which are excluded from the model form, see
        also ``get_form``.
        """
        return ("id",)

    def get_next(self, formatted=True):
        """
        Returns the next order number as string. Derived classes must implement
        this method.

        **Parameters:**

        formatted
            If True the number will be returned within the stored format, which
            is based on Python default string formatting operators, e.g.
            ``%04d``.
        """
        raise NotImplementedError

    def get_form(self, **kwargs):
        """
        Returns the form which is used within the shop preferences management
        interface.

        All parameters are passed to the form.
        """

        class OrderNumberGeneratorForm(forms.ModelForm):
            class Meta:
                model = self
                exclude = self.exclude_form_fields()

        return OrderNumberGeneratorForm(**kwargs)


class HotelOrderNumberGenerator(OrderNumberGenerator):
    last_number  = models.IntegerField(default=0)

    """
    1002 表示订房
    1003表示充值
    1004 退货
    """
    def get_next(self,prefixnumber, formatted=True):
        date_n = datetime.now().strftime('%Y%m%d%H')[2:]
        self.last_number+=1
        number = self.last_number
        self.save()
        orderNumber ='{0}{1}{2}{3}'.format(prefixnumber,date_n,number,random.randint(1, 9))
        return orderNumber

    @staticmethod
    def get_next_hotel_package_order_number(request=None):
        try:
            order_numbers = HotelOrderNumberGenerator.objects.select_for_update().get(id="order_number")
        except HotelOrderNumberGenerator.DoesNotExist:
            order_numbers = HotelOrderNumberGenerator.objects.create(id="order_number")
        return order_numbers.get_next(prefixnumber=1002)

    @staticmethod
    def get_next_pay_order():
        try:
            order_numbers = HotelOrderNumberGenerator.objects.select_for_update().get(id="order_pay_number")
        except HotelOrderNumberGenerator.DoesNotExist:
            order_numbers = HotelOrderNumberGenerator.objects.create(id="order_pay_number")
        return order_numbers.get_next(prefixnumber=1003)

    @staticmethod
    def get_next_refund_number():
        with transaction.atomic():
            try:
                refund_number = HotelOrderNumberGenerator.objects.select_for_update().get(id="refund_number")
            except HotelOrderNumberGenerator.DoesNotExist:
                refund_number = HotelOrderNumberGenerator.objects.create(id="refund_number")
            time_str = datetime.now().strftime('%Y%m%d%H')[2:]
            refund_number.last_number += 1
            refund_number.save()
            refund_number = '{0}{1}{2}'.format(1004,time_str,refund_number.last_number)
            return refund_number

    class Meta:
        app_label = 'chaolife'



