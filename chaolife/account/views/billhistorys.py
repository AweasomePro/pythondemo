#-*- coding: utf-8 -*-
from authtoken.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models import BillHistory
from common.viewsets import CustomDynamicModelViewSet
from account.serializers import BillHistorySerializer


class BillHistoryView(CustomDynamicModelViewSet):
    serializer_class = BillHistorySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = BillHistory.objects.all()


    def get_queryset(self, queryset=None):
        request = self.request
        client_type  = request.client_type
        print(client_type)
        if client_type == 'client':
            return self.queryset.filter(user=self.request.user).get_client_set()
        elif client_type == 'business':
            print('return busisenen')
            return self.queryset.filter(user=self.request.user).get_business_set()
        else:
            return self.queryset.filter(user=self.request.user)

