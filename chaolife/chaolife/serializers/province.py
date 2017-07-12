#-*- coding: utf-8 -*-
from chaolife.serializers.city import CitySerializer

from chaolife.models.province import Province
from chaolife.serializers.support import DynamicFieldsModelSerializer


class ProvinceSerializer(DynamicFieldsModelSerializer):
    citys = CitySerializer(many=True)

    class Meta:
        model= Province