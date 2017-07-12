# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_auto_20160825_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsrecord',
            name='business_type',
            field=models.IntegerField(help_text='业务类型', default=1, choices=[(1, '登入'), (2, '注册')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='smsrecord',
            name='ali_code',
            field=models.IntegerField(help_text='阿里返回的code', blank=True),
        ),
    ]
