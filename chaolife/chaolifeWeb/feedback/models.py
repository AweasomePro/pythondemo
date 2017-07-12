from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import CreateMixin
from chaolifeProject.settings import AUTH_USER_MODEL

class Feedback(CreateMixin,models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,help_text='如果已登入用户,则为主键，否则为0',null=True,blank=True)
    content = models.TextField(verbose_name=_('反馈内容'),help_text='反馈内容')

    class Meta:
        verbose_name = '反馈意见'
        verbose_name_plural ='反馈意见'

    def __str__(self):
        if self.user == None:
            return '匿名用户反馈'
        else:
            return self.user.name+'的反馈意见'