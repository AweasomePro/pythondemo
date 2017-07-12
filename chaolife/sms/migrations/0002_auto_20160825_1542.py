# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsrecord',
            name='business_id',
            field=models.UUIDField(help_text='前端发送过来验证的唯一标识', default=uuid.uuid4),
        ),
    ]
