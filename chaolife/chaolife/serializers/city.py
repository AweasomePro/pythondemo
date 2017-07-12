#-*- coding: utf-8 -*-
from chaolife.models.city import City
from dynamic_rest.serializers import DynamicModelSerializer


class CitySerializer(DynamicModelSerializer):
    class Meta:
        model = City
        exclude = ('province',)