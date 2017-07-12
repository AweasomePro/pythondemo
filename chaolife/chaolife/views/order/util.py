# -*- coding:utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView


class DeleteAllOrderView(APIView):
    def get(self,requeset,format = None):
        from chaolife.models import Order
        Order.objects.all().delete()
        return Response(data='success')