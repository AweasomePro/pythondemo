from django.db import models

class TypeModel(models.Model):

    name = models.CharField(null=False,blank=False,default='商务大床房')