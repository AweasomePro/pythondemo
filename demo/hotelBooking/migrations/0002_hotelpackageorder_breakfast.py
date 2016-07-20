# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpackageorder',
            name='breakfast',
            field=models.IntegerField(default=1, verbose_name='早餐类型', help_text=' 订单生成时,所记录的早餐类型'),
        ),
    ]
