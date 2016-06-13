from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission
from .helper.fiels import ListField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,phone,name,password=None):
        if not phone:
            raise ValueError('User must have an phone')
        user = self.model(phone = phone)
        user.set_password(raw_password=password)
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        user = self.create_user(phone,name, password)
        user.is_active = True
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    phone = models.CharField(max_length=15,unique=True)
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_active = models.BigIntegerField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group,blank=True)
    permissions = models.ManyToManyField(Permission,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name',]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

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

    def __unicode__(self):
        return self.phone

class Member(User):
    # name = models.CharField(max_length=50)
    # phoneNumber = models.BigIntegerField()
    # phoneNumberIsVerify = models.BooleanField(default=False)
    registerTime = models.DateTimeField(auto_now_add=True)
    objects = UserManager



class Installation(models.Model):
    badge = models.BigIntegerField(null=True,default=0)
    channels = ListField(default=[])
    deviceProfile = models.CharField(max_length=200,default="")
    deviceToken = models.CharField(max_length=200,unique=True,null=True)
    deviceType = models.CharField(max_length=200,default="")
    installationId = models.CharField(max_length=200,unique=True,null=True)
    timeZone = models.CharField(max_length=200,null=True,default="")
    # member = models.ForeignKey(Member,null=True,default=1)

class Hotel(models.Model):
    # 指定 主键 primary_key =True
    pass





