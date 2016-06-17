from rest_framework import serializers

# username = models.CharField(max_length=50)
# password = models.CharField(max_length=30)
# email = models.EmailField
# phoneNumber = models.IntegerField(max_length=15)
# register_time = models.DateTimeField(auto_created=True)

from .models import  User,Installation, Province, City, Hotel,House,HotelLogoImg,HouseImg,HousePackage


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self,*args,**kwargs):
        #Don't pass the 'fiels' arg up tp the superclass
        fields = kwargs.pop('fields',None)
        exclude = kwargs.pop('excludes', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args,**kwargs)

        if fields is not None :
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude is not None:
            existing = set(self.fields.keys())
            disallowed = set(exclude)
            for field_name in existing & disallowed:
                self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name','phone_number','create_at')

class InstallationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Installation
        # choices = {'badge','deviceProfile','installationId','timeZone'}

class HotelImgSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = HotelLogoImg
        exclude =('id',)

class HouseImgSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = HouseImg
        exclude=('id',)

class HousePackageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = HousePackage
        exclude=('id',)

class HouseSerializer(DynamicFieldsModelSerializer):
    houseImgs = HouseImgSerializer(many=True)
    housePackages = HousePackageSerializer(many=True)
    class Meta:
        model = House


class HotelSerializer(DynamicFieldsModelSerializer):
    hotelLogoImgs = HotelImgSerializer(many=True)

    houses = HouseSerializer(many=True, excludes=('hotel',))
    class Meta:
        model = Hotel


class CitySerializer(DynamicFieldsModelSerializer):
    hotels = HotelSerializer(many=True)

    class Meta:
        model = City
        exclude = ('province',)


class ProvinceSerializer(DynamicFieldsModelSerializer):
    citys = CitySerializer(many=True,excludes=('hotels',))

    class Meta:
        model= Province











