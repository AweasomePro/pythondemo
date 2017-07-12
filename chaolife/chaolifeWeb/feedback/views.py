from rest_framework import viewsets
from common.utils.AppJsonResponse import DefaultJsonResponse
from .models import Feedback
from .serializers import FeedbackSerializer
class FeedbackView(viewsets.mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if request.user:
            print('has user')
            print(request.user)
            data = data.copy()
            data['user'] = request.user.id
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return DefaultJsonResponse(serializer.data, status=201, headers=headers)
        else:
            from chaolife.exceptions import ConditionDenied
            raise ConditionDenied('暂不支持,匿名用户')
