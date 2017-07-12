from django.db.models.signals import pre_save
from django.dispatch import receiver
from ..models import SmsRecord
# @receiver(pre_save,sender= SmsRecord)
# def smsRecord_pre_save(sender,instance=None,**kwargs):
#     smsRecord = instance
#     ali_template_code = smsRecord.ali_template_code
