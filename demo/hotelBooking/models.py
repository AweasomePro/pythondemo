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
    badge = models.BigIntegerField()
    channels = ListField()
    deviceProfile = models.CharField(max_length=200)
    deviceToken = models.CharField(max_length=200,unique=True)
    deviceType = models.CharField(max_length=200)
    installationId = models.CharField(max_length=200,unique=True)
    timeZone = models.CharField(max_length=200)



