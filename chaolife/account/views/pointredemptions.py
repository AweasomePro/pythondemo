#-*- coding: utf-8 -*-
from chaolife.exceptions import ConditionDenied
from common.utils.AppJsonResponse import DefaultJsonResponse
from common.viewsets import CustomDynamicModelViewSet
from ..serializers import PointRedemptionSerializer
from ..models import PointRedemption
from django.db import transaction
from common import appcodes
class PointRedemptionsViewSet(CustomDynamicModelViewSet):
    serializer_class = PointRedemptionSerializer
    queryset = PointRedemption.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.pointredemption_set and user.pointredemption_set.filter(state__in=(PointRedemption.STATE_REQUIRE,PointRedemption.STATE_ACCEPT)).exists():
            raise ConditionDenied(detail='存在正在处理的请求,',code=appcodes.CODE_EXISTE_UNHANDLE_REDEMPTIONS)
        data = request.data.copy()
        with transaction.atomic():
            data['user'] = request.user.id
            data['state'] = PointRedemption.STATE_REQUIRE
            serializer = self.get_serializer(data=data,context ={'request':request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return DefaultJsonResponse(serializer.data, headers=headers)


