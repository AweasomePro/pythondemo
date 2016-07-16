from datetime import datetime

from django import forms
from django.db import models
from hotelBooking.models import BaseModel

productTypeMap = {
    "hotelPackage":"01"
}

"""
订单号规则:
年后2位+月份+日期+当天订单数量+商品类型+随机数
"""
class OrderNumberGenerator(BaseModel):
    id = models.CharField(primary_key=True,max_length=20)

    class Meta:
        app_label = 'hotelBooking'
        abstract = True

    def init(self,request,order):
        self.request = request
        self.order = order
        self.user = request.user

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

    def get_next(self, formatted=True):
        str = datetime.now().strftime('%Y%m%d%H')[2:]
        self.last_number+=1
        number = self.last_number
        self.save()
        orderNumber ='{0}{1}{2}'.format(1002,str,number)
        return int(orderNumber)

    class Meta:
        app_label = 'hotelBooking'

class test(BaseModel):
    pass


