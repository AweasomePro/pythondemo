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


class UserSerializer(DynamicFieldsModelSerializer):
    name =  serializers.CharField(read_only=False, required=False, allow_null=True,)
    phone_number = serializers.CharField(read_only=True,required=False)
    password = serializers.CharField(write_only=True,required=False)
    create_at= serializers.DateTimeField(read_only=True,required=False)
    avatar = serializers.URLField(required=False)

    class Meta:
        model = User
        # write_only_fields = ('password',)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.avatar = validated_data.get('avatar',instance.avatar)
        return instance


class UpdateUserSerializer(UserSerializer):
    exclude = ('password','groups',"is_admin","is_active")


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











