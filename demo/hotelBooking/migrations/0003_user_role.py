# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0002_hotelpackageorder_breakfast'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(help_text='该账号的角色标识', choices=[(1, '顾客'), (2, '合作伙伴')], default=1),
        ),
    ]
