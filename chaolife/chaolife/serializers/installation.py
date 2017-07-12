#-*- coding: utf-8 -*-
from account.models import Installation
from chaolife.serializers.support import DynamicFieldsModelSerializer
from rest_framework import serializers


class InstallationSerializer(DynamicFieldsModelSerializer):
    channels = serializers.ListField()
    class Meta:
        model = Installation

    def is_valid(self, raise_exception=True):
        return super(InstallationSerializer,self).is_valid(raise_exception)

    def save(self, **kwargs):
        #todo 判断如何存在 不save
        initial_data = self.initial_data
        deviceType = initial_data.get('deviceType')
        if (deviceType == 'android'):
            try:
                installation = Installation.objects.get(deviceType='android', installationId=initial_data.get('installationId'))
            except Installation.DoesNotExist:
                return super(DynamicFieldsModelSerializer,self).save(**kwargs)
            else:
                return self.update(installation,self.validated_data)
        elif(deviceType=='ios'):
            try:
                installation = Installation.objects.get(deviceType='ios', deviceToken=initial_data.get('deviceToken'))
            except Installation.DoesNotExist:
                return super(DynamicFieldsModelSerializer,self).save(**kwargs)
            else:
                print(self.validated_data)
                return self.update(installation,self.validated_data)