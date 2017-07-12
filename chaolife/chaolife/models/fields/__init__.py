from .points import PointField
from django.db.models import fields
from django.core import exceptions, validators, checks
from django.utils.translation import ugettext_lazy as _
from time import strptime

class HourField(fields.CharField):

    support_hours = (
        ('14:00','14:00'),
        ('15:00','15:00'),
        ('16:00','16:00'),
        ('17:00','17:00'),
        ('18:00','18:00'),
        ('19:00','19:00'),
        ('20:00','20:00'),
        ('21:00','21:00'),
        ('22:00','22:00'),
        ('23:00','23:00'),
        ('24:00','24:00'),
    )

    def __init__(self,*args,**kwargs):
        kwargs.update({
            'max_length':255,
            'choices': self.support_hours,
            'default': self.support_hours[0][0],
        })
        super(HourField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(HourField, self).check(**kwargs)
        errors.extend(self.__check_hours())
        return errors

    def __check_hours(self):
        return []


