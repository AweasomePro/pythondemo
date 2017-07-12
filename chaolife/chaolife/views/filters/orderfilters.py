import django_filters
from ...models import HotelPackageOrder
class HotelOrderFilter(django_filters.FilterSet):
    class Meta:
        HotelPackageOrder
        fields = ()
