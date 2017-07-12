from django.shortcuts import render

from common.utils.AppJsonResponse import DefaultJsonResponse
from common.viewsets import CustomDynamicReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from .serializers import ApkSerializer
from .models import Apk
from rest_framework.decorators import list_route
# Create your views here.


class ApkViewSets(CustomDynamicReadOnlyModelViewSet):
    serializer_class = ApkSerializer
    queryset = Apk.objects.all()

    @list_route(methods=['get'],url_path='latest')
    def latest_version(self,request,*args,**kwargs):
        apk_type = request.GET.get('apk-type',Apk.Android)
        client_type = request.GET.get('client',0)
        apk = self.queryset.filter(type=apk_type,client=client_type).first()
        if apk!= None:
            return DefaultJsonResponse(data=self.get_serializer_class()(apk).data)
        else:
            return DefaultJsonResponse(data=None,message='无apk')