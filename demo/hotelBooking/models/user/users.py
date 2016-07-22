from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from hotelBooking.core.exceptions import UserCheck
from hotelBooking.core.fields.pointField import PointField
from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission
from enumfields import Enum, EnumIntegerField
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone_number, name = 'AnymousName', password=None):
        if not phone_number:
            raise ValueError('User must have an phone')
        UserCheck.validate_phoneNumber(phone_number)
        user = self.model(phone_number = phone_number)
        user.set_password(raw_password=password)
        user.name = name
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, name, password):
        user = self.create_user(phone_number=phone_number,name=name, password=password)
        user.is_active = True
        user.is_admin = True
        user.save()
        return user


class PointMixin(models.Model):

    def deductPoint(self,point):
        self.point -= point

    class Meta:
        app_label = 'hotelBooking'
        abstract = True

class User(PointMixin,PermissionsMixin,AbstractBaseUser):
    male = 1
    female = 0
    CUSTOMER = 1
    HOTEL_PARTNER = 2
    SEX = (
        (male,'male'),
        (female,'female'),
    )
    ROLE = (
        (CUSTOMER,'顾客'),
        (HOTEL_PARTNER,'酒店代理合作伙伴'),
    )

    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=225,default="unknow name")
    email = models.EmailField(max_length=255,blank=True)
    sex = models.IntegerField(default=male,choices=SEX)
    phone_is_verify = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_loggin = models.BooleanField(default=False)
    role  = models.IntegerField( choices=ROLE,default=ROLE[0][0],help_text='该账号的角色标识')
    create_at = models.DateTimeField(auto_now_add=True)
    point = PointField(default=0,editable=False,verbose_name='积分')
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name',]

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_username(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        if self.is_active:
            return True
        else:
            return False

    def has_module_perms(self,app_label):
        if self.is_admin and self.is_active:
            return True
        else:
            return False

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_customer_member(self):
        # todo  使用数据库 字段 来优化
        return self.customermember is not None or self.role ==self.CUSTOMER


    def __unicode__(self):
        return self.phone_number

    @staticmethod
    def existPhoneNumber(phone_number = None):
        try:
            User.objects.get(phone_number=phone_number)
            return True
        except User.DoesNotExist:
            return False

class ProductMemberType(Enum):
    HotelAgent = 1

    class Labels:
        HotelAgent = _('酒店代理')


class MemberManager(models.Manager):

    def create(self,phoneNumber,password):
        user = User.objects.create_user(phoneNumber)
        user.set_password(raw_password=password)
        member = CustomerMember()
        member.user = user
        member.save()
        if (user.check_password(raw_password=password)):
            print('验证成功')
        else:
            print('验证失败')
        return member

class CustomerMember(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    avatar = models.URLField(blank=True)
    last_access = models.DateTimeField(_("Last accessed"), default=timezone.now)
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
    user = models.OneToOneField(User,primary_key=True)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = '加盟会员'
        verbose_name_plural = '加盟会员'

    def __str__(self):
        return self.user.name+'-'+ str(self.user.phone_number)





