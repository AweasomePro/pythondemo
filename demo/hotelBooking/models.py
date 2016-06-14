from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Group,Permission
from .helper.fiels import ListField
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
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=225,default="unknow name")
    email = models.EmailField(max_length=255)
    phone_is_verify = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_active = models.BigIntegerField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group,blank=True)
    permissions = models.ManyToManyField(Permission,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name',]

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

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
        return self.phone_number

# class Member(User):
    # name = models.CharField(max_length=50)
    # phoneNumber = models.BigIntegerField()
    # phone_is_verify = models.BooleanField(default=False)
    # objects = UserManager



class Installation(models.Model):
    badge = models.BigIntegerField(null=True,default=0,verbose_name='ios badge数')
    channels = ListField(default=[],verbose_name='订阅渠道')
    deviceProfile = models.CharField(max_length=200,default="")
    deviceToken = models.CharField(max_length=200,unique=True,null=True)
    deviceType = models.CharField(max_length=200,default="")
    installationId = models.CharField(max_length=200,unique=True,null=True,verbose_name='设备id')
    timeZone = models.CharField(max_length=200,null=True,default="")
    user = models.ForeignKey(User,null=True,default=-1,verbose_name='绑定用户')

    class Meta:
        verbose_name = "App已安装设备"
        verbose_name_plural = "设备"

    def __unicode__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    def __str__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)



class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False)
    name_py = models.CharField(max_length=200,null=False)

    class Meta:
        verbose_name = "省份"
        verbose_name_plural = "省份"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name



class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False,verbose_name='城市字母拼音')
    name_py = models.CharField(max_length=200, null=False,verbose_name='城市中文拼音')
    province = models.ForeignKey(Province,verbose_name='所属省份',related_name='citys')

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = "城市"

    def __unicode__(self):
        return self.name


class Hotel(models.Model):

    # 指定 主键 primary_key =True
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,verbose_name='所在城市',related_name='hotels')
    name = models.CharField(max_length=200,null=False,verbose_name='酒店名')
    address = models.CharField(max_length=255,null=False)
    introduce = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    introduce_imgs = ListField(verbose_name='展示图片(数组)')

    class Meta:
        verbose_name = "酒店"
        verbose_name_plural = "酒店"

HotelType =((1,'商务豪华'),(2,'商务普通'))

class House(models.Model):
    """
    这个类表示发布的房源信息
    """
    hotel = models.ForeignKey(Hotel,verbose_name='所属酒店',related_name='houses')
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = "房源"
        verbose_name_plural = "房源"
    pass

class Booking(models.Model):
    pass





