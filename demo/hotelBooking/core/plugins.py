import math
from django import forms
from django.db import models
from datetime import datetime
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
    last_day = models.DateTimeField(default=None)
