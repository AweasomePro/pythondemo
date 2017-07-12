# -*- coding:utf-8 -*-
from chaolife.serializers import RoomDayStateSerializer
from rest_framework import viewsets,views

class RoomStateView(viewsets.ModelViewSet):
    serializer_class = RoomDayStateSerializer
