from django.db import models
from django.contrib.auth.models import User, UserManager
from .helper.fiels import ListField
# Create your models here.


class Member(User):
    name = models.CharField(max_length=50)
    phoneNumber = models.BigIntegerField()
    phoneNumberIsVerify = models.BooleanField(default=False)
    registerTime = models.DateTimeField(auto_now_add=True)
    objects = UserManager


class Installation(models.Model):
    badge = models.BigIntegerField(null=True,default=0)
    channels = ListField(default=[])
    deviceProfile = models.CharField(max_length=200,default="")
    deviceToken = models.CharField(max_length=200,unique=True,null=True,default="")
    deviceType = models.CharField(max_length=200,default="")
    installationId = models.CharField(max_length=200,unique=True,null=True)
    timeZone = models.CharField(max_length=200,null=True,default="")
    member = models.ForeignKey(Member,null=True,default=-1,blank=True)





