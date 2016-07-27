from hotelBooking.models.installation import Installation
from hotelBooking.serializers.support import DynamicFieldsModelSerializer


class InstallationSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Installation