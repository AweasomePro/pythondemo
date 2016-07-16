from dynamic_rest.fields import DynamicRelationField, DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from hotelBooking.models.user import User,CustomerMember
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict


class CustomerMemberSerializer(DynamicModelSerializer):
    class Meta:
        model = CustomerMember
        fields = ('avatar',)


class UpdateMemberSerializer(DynamicModelSerializer):
    avatar = DynamicMethodField(
        requires=['customermember.avatar', ]
    )
    class Meta:
        model = User
        fields = ('name','sex','avatar')

    def get_avatar(self, user):
        return user.customermember.avatar

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.sex = validated_data.get('sex',instance.sex)
        # instance.customermember.avatar = validated_data.get('avatar', instance.avatar)
        return instance

class CustomerUserSerializer(DynamicModelSerializer):
    avatar = DynamicMethodField(
        requires = ['customermember.avatar',]
    )
    def get_avatar(self,user):
        return user.customermember.avatar
    class Meta:
        model = User
        name = 'user'
        fields = ('id','name','phone_number','point','sex','avatar',)

