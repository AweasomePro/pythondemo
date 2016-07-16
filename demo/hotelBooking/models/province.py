from django.db import models

class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "省份"
        verbose_name_plural = "省份"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
