from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from chaolife.exceptions import NotExistUser,PayPwdError,UserCheck
from .fields import PointField
from common.fiels import ListField

# Create your models here.
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name = 'AnymousName', password=None):
        if not phone_number:
            raise ValueError('User must have an phone')
        UserCheck.validate_phoneNumber(phone_number)
        user = self.model(phone_number = phone_number,is_active=True,)
        user.set_password(raw_password=password)
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password):
        user = self.create_user(phone_number=phone_number,name=name, password=password)
        user.is_admin = True
        user.save()
        return user

    def create_hotel_partner(self,phone_number,name,deposit):
        import random
        user = self.create_user(phone_number=phone_number, name=name, password=str(random.randint(1000000,9999999)))
        user.save()
        return user
        pass

    def set_user_is_customer(self, ):
        CustomerMember.objects.create_for_exist_user(self)


    def get_or_create(self,phone_number,**kwargs):

        pass

    def exist_user(self,phone_number):
        try:
            self.model.objects.get(phone_number= phone_number)
            return True
        except self.model.DoesNotExist:
            return False


class CustomerPointMixin(models.Model):
    points = PointField(default=0, verbose_name='积分',)
    consumptions = models.PositiveIntegerField(verbose_name='消费金额',default=0,null=True,blank=True)
    invoiced_consumptions = models.PositiveIntegerField(verbose_name='已开票金额',default=0,null=True,blank=True)

    def deduct_point(self, point):
        self.points = self.points - point
        self.save()

    def add_point(self, point):
        self.points = self.points + point
        self.save()

    class Meta:
        app_label = 'chaolife'
        abstract = True


class PartnerPointMixin(models.Model):
    points = models.PositiveIntegerField(default=0,verbose_name='积分')
    invoice = models.PositiveIntegerField(default=0,verbose_name='可开积分余额',help_text='客户向我方邮寄的发票转换的可开积分余额')
    deposit = MoneyField(max_digits=6,decimal_places=2)
    deposit_points = models.IntegerField(default=0, verbose_name='押金积分')

    class Meta:
        abstract=True

    def deduct_point(self, point):
        """
        只负责减掉积分,do not care why
        :param point:
        :return:
        """
        if self.points < point: #当前账号积分小于，需要从deposi_point中扣除
            # warn should send email to warn admin
            deduct_deposit_point = point - self.points
            self.deposit_points -= deduct_deposit_point
            self.points = 0
        else:
            self.points-=point
        self.save()

    def add_point(self, point):
        if self.deposit_points < 30000: #当前押金积分小于30000分 先补充至押金
            need_made_up_points = 30000 -self.deposit_points
            if need_made_up_points > point:
                self.deposit_points += point
            else:
                self.deposit_points = 30000
                self.points += point - need_made_up_points
        else:
            self.points = self.points + point
        self.save()

    class Meta:
        app_label = 'chaolife'
        abstract = True




class User( PermissionsMixin, AbstractBaseUser):
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
    pay_pwd =  models.CharField(_('password'), max_length=6, default='000000')
    email = models.EmailField(max_length=255,blank=True)
    sex = models.IntegerField(default=male,choices=SEX)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_login = models.BooleanField(default=False)
    profile_integrity = models.BooleanField(default=False)
    role  = models.IntegerField( choices=ROLE,default=ROLE[0][0],help_text='该账号的角色标识')
    create_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name',]

    class Meta:
        app_label = 'account'
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
        return self.role > 0

    @property
    def is_partner_member(self):
        return self.role == self.HOTEL_PARTNER

    def add_customer_points(self,points):
        if self.customermember:
            self.customermember.points += points
            self.customermember.save()

    def add_partner_points(self,points):
        if self.partnermember:
            if points >0:
                self.partnermember.add_point(points)
            else:
                self.partnermember.deduct_point(abs(points))
        else:
            raise RuntimeError('错误的情况发生')

    def __str__(self):
        return self.phone_number

    def __unicode__(self):
        return self.phone_number

    @property
    def lean_push_json(self):
        installation = self.installation_set.filter()
        return 'nothing,to delete'


    @property
    def max_redemption_points(self):
        pass

    @staticmethod
    def existPhoneNumber(phone_number = None,raise_exception = True):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user:
                return True
        except User.DoesNotExist:
            if(not raise_exception):
                return False
            else:
                raise NotExistUser()
    @staticmethod
    def check_smscode(phone_number,smsCode):
        from message import verify_sms_code
        success,res = verify_sms_code(phone_number,smsCode)
        if(success):
            return True
        else:
            return False

    def check_pay_pwd(self,pwd):
        if self.pay_pwd!=str(pwd):
            raise PayPwdError()
        return True

    def set_pay_pwd(self,pwd):
        self.pay_pwd = pwd
        self.save(update_fields=('pay_pwd',))




class MemberManager(models.Manager):

    def create(self,phoneNumber):
        user = User.objects.create_user(phoneNumber)
        member = CustomerMember()
        member.user = user
        member.save()
        return member


    def create_for_exist_user(self,user):
        member = CustomerMember(user=user)
        member.save()

class CustomerMember(CustomerPointMixin,models.Model):
    """
    实际上就像一个 profile
    """
    user = models.OneToOneField(User,primary_key=True)
    avatar = models.URLField(blank=True)

    objects = MemberManager()

    def __init__(self,*args,**kwargs):
        super(CustomerMember,self).__init__(*args,**kwargs)

    class Meta:
        app_label = 'account'
        verbose_name = '会员'
        verbose_name_plural = '会员'

    def update_avatar_url(self,url):
        self.avatar = url
        self.save(update_fields=('avatar',))


    @property
    def max_invoices_value(self):
        return self.consumptions - self.invoiced_consumptions

    def __str__(self):
        return self.user.name+'-'+str(self.user.phone_number)



class PartnerMember(PartnerPointMixin,models.Model):
    user = models.OneToOneField(User,primary_key=True)
    class Meta:
        app_label = 'account'
        verbose_name = '加盟会员'
        verbose_name_plural = '加盟会员'

    def __str__(self):
        return self.user.name+'-'+ str(self.user.phone_number)







