from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers
# username = models.CharField(max_length=50)
# password = models.CharField(max_length=30)
# email = models.EmailField
# phoneNumber = models.IntegerField(max_length=15)
# register_time = models.DateTimeField(auto_created=True)
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.validators import UniqueValidator

from .models import  User
from . import Installation, Province, City, Hotel,House,HotelImg,HouseImg,HousePackage,CustomerMember

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

    class Meta:
        model = User
        excludes=('',)
        readonly = ()


class CustomerMemberSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(read_only=True,required=False)
    user = UserSerializer()
    avatar = serializers.URLField(read_only=False,required=False)

    class Meta:
        model = CustomerMember
        excludes=('is_admin','is_active','is_loggin',)
        # write_only_fields = ('password',)

    def update(self, instance, validated_data):
        instance.user.name = validated_data.get('name',instance.name)
        instance.avatar = validated_data.get('avatar',instance.avatar)
        return instance

    @property
    def data(self):
        ret = super(DynamicFieldsModelSerializer, self).data
        user_dict = ret.pop('user')
        ret.update(user_dict)
        for field_name in self.Meta.excludes:
            ret.pop(field_name)
        return ReturnDict(ret, serializer=self)

class UpdateCustomerMemberSerializer(CustomerMemberSerializer):

    exclude = ('password','groups',"is_admin","is_active")


class InstallationSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Installation


        # choices = {'badge','deviceProfile','installationId','timeZone'}



# class HotelImgSerializer(DynamicModelSerializer):
#
#     class Meta:
#         model = HotelImg
#         name = 'hotel_img'
#         exclude =()
#
#
# class HouseImgSerializer(DynamicModelSerializer):
#
#     class Meta:
#         model = HouseImg
#         exclude_fields=('id',)
#
#
# class HousePackageSerializer(DynamicModelSerializer):
#
#     class Meta:
#         model = HousePackage
#         exclude_fields=()
#
#
# class HouseSerializer(DynamicModelSerializer):
#     house_imgs = HouseImgSerializer(many=True,embed=True)
#     housePackages = HousePackageSerializer(many=True,exclude_fields=('house','product'),embed=True)
#     class Meta:
#         model = House
#
#
# class HotelSerializer(DynamicModelSerializer):
#     # hotel_imgs = HotelImgSerializer(many=True)
#     # hotel_houses = HouseSerializer(many=True)
#     hotel_imgs = HotelImgSerializer(embed=True,many=True,exclude_fields=('id','hotel'))
#     hotel_houses = HouseSerializer(many=True,embed=True,only_fields=('id',))
#     class Meta:
#         model = Hotel
#         name = 'hotel'
#
#     # def to_representation(self, instance):
#     #     return instance

#
# class CitySerializer(DynamicFieldsModelSerializer):
#     hotels = HotelSerializer(many=True)
#
#     class Meta:
#         model = City
#         exclude = ('province',)
#
#
# class ProvinceSerializer(DynamicFieldsModelSerializer):
#     citys = CitySerializer(many=True,excludes=('hotels',))
#
#     class Meta:
#         model= Province











