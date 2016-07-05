from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission

from hotelBooking.core.fields.pointField import PointField
from .utils.fiels import ListField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError('User must have an phone')
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


class User(AbstractBaseUser):
    male = 1
    female = 0
    SEX = (
        (male,'male'),
        (female,'female'),
    )

    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=225,default="unknow name")
    email = models.EmailField(max_length=255,blank=True)
    sex = models.IntegerField(default=male,choices=SEX)
    phone_is_verify = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_loggin = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    point = PointField(default=0,editable=False,verbose_name='积分')
    groups = models.ManyToManyField(Group,blank=True,default=None)
    permissions = models.ManyToManyField(Permission,blank=True)
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
        return self.customermember is not None

    def __unicode__(self):
        return self.phone_number

    @staticmethod
    def existPhoneNumber(phone_number = None):
        return User.objects.filter(phone_number = phone_number).exists()










