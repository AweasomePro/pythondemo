# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_auto_20160825_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsrecord',
            name='business_type',
            field=models.IntegerField(choices=[(1, '登入'), (2, '注册'), (3, '重置支付密码')], help_text='业务类型'),
        ),
    ]
