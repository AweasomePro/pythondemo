from dynamic_rest.fields import DynamicRelationField, DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from account.models import User,BillHistory
from rest_framework import serializers
class UserSerializer(DynamicModelSerializer):

    class Meta:
        model = User
        name = 'user'
        fields = ('id','name','phone_number','point','sex',)


class UpdateMemberSerializer(DynamicModelSerializer):
    avatar = DynamicMethodField(
        requires=['customermember.avatar', ],required=False
    )
    pay_pwd = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = User
        fields = ('name','sex','avatar','pay_pwd')


    def get_avatar(self, user):
        return user.customermember.avatar

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.sex = validated_data.get('sex',instance.sex)
        instance.pay_pwd = validated_data.get('pay_pwd',instance.pay_pwd)
        instance.active = True
        instance.profile_integrity = True
        instance.save()
        instance.customermember.save()
        return instance


class CustomerUserSerializer(DynamicModelSerializer):
    avatar = DynamicMethodField(
        requires = ['customermember.avatar',]
    )

    def get_avatar(self,user):
        return user.customermember.avatar

    points = DynamicMethodField()
    consumptions = DynamicMethodField()

    def get_points(self,user):
        return user.customermember.points
    def get_consumptions(self,user):
        return user.customermember.consumptions

    class Meta:
        model = User
        name = 'user'
        fields = ('id','name','phone_number','points','sex','avatar','profile_integrity','consumptions')


class PartnerUserSerializer(DynamicModelSerializer):
    points = DynamicMethodField(
    )
    invoice = serializers.IntegerField(source='partnermember.invoice')
    deposit_points = serializers.IntegerField(source='partnermember.deposit_points')

    def get_points(self,user):
        return user.partnermember.points

    class Meta:
        model = User
        name = 'user'
        fields = ('id','name','phone_number','points','deposit_points','sex','profile_integrity','invoice')