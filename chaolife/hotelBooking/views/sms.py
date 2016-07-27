from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import detail_route,list_route

class SmsAPIView(APIView):

    def get(self,request,):

        return Response('success')