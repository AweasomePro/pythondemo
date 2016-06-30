from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission
from . import User
from enumfields import Enum, EnumIntegerField
from django.utils.translation import ugettext_lazy as _
class ProductMemberType(Enum):
    HotelAgent = 1

    class Labels:
        HotelAgent = _('酒店代理')


class MemberManager(models.Manager):

    def create(self,phoneNumber,password):
        user = User()
        user.phone_number = phoneNumber
        user.password = password
        user.save()
        member = CustomerMember()
        member.user = user
        member.save()
        return member



class CustomerMember(models.Model):
    avatar = models.URLField(blank=True)
    user = models.OneToOneField(User)

    objects = MemberManager()

    def __init__(self,*args,**kwargs):
        super(CustomerMember,self).__init__(*args,**kwargs)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = '会员'
        verbose_name_plural = '会员'


class FranchiseeMember(models.Model):
    user = models.OneToOneField(User)
    type = EnumIntegerField(ProductMemberType, default = ProductMemberType.HotelAgent,verbose_name = _('加盟商类型'))

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = '加盟会员'
        verbose_name_plural = '加盟会员'

