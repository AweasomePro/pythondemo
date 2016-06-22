# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotelBooking', '0010_auto_20160617_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, auto_created=True, parent_link=True, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('hotelBooking.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True),
        ),
    ]
