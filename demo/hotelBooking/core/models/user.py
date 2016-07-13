from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission
from hotelBooking.models import User
from enumfields import Enum, EnumIntegerField
from django.utils.translation import ugettext_lazy as _
class ProductMemberType(Enum):
    HotelAgent = 1

    class Labels:
        HotelAgent = _('酒店代理')


class MemberManager(models.Manager):

    def create(self,phoneNumber,password):
        user = User.objects.create_user(phoneNumber,password=password)
        member = CustomerMember()
        member.user = user
        member.save()
        if (user.check_password(raw_password=password)):
            print('验证成功')
        else:
            print('验证失败')
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


    def update_avatar_url(self,url):
        self.avatar = url
        self.save(update_fields=('avatar',))
    # @staticmethod
    # def update_user_avatar(phone_number,avatar_url):
    #     User.objects.get(phone_number= phone_number)
    #     member = CustomerMember.objects.get='phone_number')
    #     member.avatar = avatar_url
    #     member.save()

    def __str__(self):
        return self.user.name+'-'+str(self.user.phone_number)

class PartnerMember(models.Model):
    user = models.OneToOneField(User)
    type = EnumIntegerField(ProductMemberType, default = ProductMemberType.HotelAgent,verbose_name = _('加盟商类型'))

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = '加盟会员'
        verbose_name_plural = '加盟会员'

    def __str__(self):
        return self.user.name+'-'+ str(self.user.phone_number)
