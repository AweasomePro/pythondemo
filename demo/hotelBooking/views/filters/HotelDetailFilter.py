from rest_framework.filters import BaseFilterBackend


class RoomDayStateFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user =request.user
        checkinTime = request.GET.get('checkinTime',None)
        checkoutTime= request.GET.get('checkoutTime',None)
        if(checkinTime and checkoutTime):
            queryset.filter()