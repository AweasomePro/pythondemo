from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Member(User):
    name = models.CharField(max_length=50)
    phoneNumber = models.IntegerField()
    phoneNumberIsVerify = models.BooleanField(default=False)
    registerTime = models.DateTimeField(auto_now_add=True)

