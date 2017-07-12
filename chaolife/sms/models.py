from django.db import models
from account.models.user import User
from sms import config
# Create your models here.
import uuid

class SmsRecord(models.Model):
    SMS_TYPE_VERTIFY = 1 # 验证类

    SMS_SEND_WAIT_VERTIFY = 2 # 等待验证
    SMS_VERTIFY_SUCCESS = 3 # 验证成功
    SMS_SEND_FAILED = -1 # 发送失败
    SMS_SEND_SUCCESS = 1 # 发送成功

    SMS_STATE_CHOICES = (
        (SMS_SEND_SUCCESS,'发送成功'),
        (SMS_SEND_FAILED,'发送失败'),
        (SMS_SEND_WAIT_VERTIFY,'等待验证'),
        (SMS_VERTIFY_SUCCESS,'验证成功'),
    )
    BUSINESS_TYPE_LOGIN = 1
    BUSINESS_TYPE_REGISTE = 2
    BUSINESS_TYPE_RESET_PAY_PWD = 3

    BUSINESS_TYPE = (
        (BUSINESS_TYPE_LOGIN,'登入'),
        (BUSINESS_TYPE_REGISTE,'注册'),
        (BUSINESS_TYPE_RESET_PAY_PWD,'重置支付密码'),

    )

    # warn todo  添加短信重置支付密码
    business_type_mapping = {
        config.template_login_code:BUSINESS_TYPE_LOGIN,
        config.template_register_code:BUSINESS_TYPE_REGISTE,
        config.template_reset_pay_pwd_code:BUSINESS_TYPE_RESET_PAY_PWD
    }


    business_id = models.UUIDField(help_text='前端发送过来验证的唯一标识',default=uuid.uuid4)

    business_type = models.IntegerField(help_text='业务类型',choices=BUSINESS_TYPE)
    phone_number = models.CharField(max_length=20,help_text='发送的手机号')
    user = models.ForeignKey(User,help_text='发送给的用户',null=True,on_delete=models.SET_NULL)
    state = models.IntegerField(choices=SMS_STATE_CHOICES)
    vertify_code = models.CharField(max_length=10,verbose_name='验证码')
    ali_code = models.IntegerField(help_text='阿里返回的code',blank=True)
    ali_template_code = models.CharField(max_length=100,help_text='发送时的短信模板')
    ali_sub_code = models.CharField(max_length=100,help_text='阿里返回的sub_code')
    ali_sub_msg = models.CharField(max_length=100,help_text='阿里返回的sub_msg')


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id == None: # 是新创建的
            print('是新创建的')
            self._set_business_type()
        super(SmsRecord,self).save(force_insert,force_update,using,update_fields)

    def _set_business_type(self):
        ali_template_code = self.ali_template_code
        self.business_type = self.business_type_mapping.get(ali_template_code)

