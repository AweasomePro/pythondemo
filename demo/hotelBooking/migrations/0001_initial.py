# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.core.models.user
import hotelBooking.core.fields
import hotelBooking.core.fields.pointField
import hotelBooking.core.models.products
import enumfields.fields
import django.utils.timezone
import hotelBooking.utils.fiels
import hotelBooking.core.models.orders
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('phone_number', models.CharField(unique=True, max_length=15)),
                ('name', models.CharField(default='unknow name', max_length=225)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(verbose_name='积分', default=0, editable=False)),
                ('groups', models.ManyToManyField(to='auth.Group', default=None, blank=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.IntegerField(verbose_name='城市代号', unique=True)),
                ('name', models.CharField(verbose_name='城市', max_length=200)),
                ('name_py', models.CharField(verbose_name='城市拼音', max_length=200)),
                ('logo', models.URLField(verbose_name='城市Logo图', default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('avatar', models.URLField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '会员',
                'verbose_name_plural': '会员',
            },
        ),
        migrations.CreateModel(
            name='FranchiseeMember',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', enumfields.fields.EnumIntegerField(verbose_name='加盟商类型', default=1, enum=hotelBooking.core.models.user.ProductMemberType)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
                ('city', models.ForeignKey(to='hotelBooking.City', verbose_name='所在城市', related_name='hotels')),
            ],
            options={
                'verbose_name': '酒店',
                'verbose_name_plural': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='房型', related_name='house_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HotelPackgeOrderSnapShot',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='房型', default='未定义房型名', max_length=255)),
                ('hotel', models.ForeignKey(to='hotelBooking.Hotel', verbose_name='所属酒店', related_name='hotel_houses')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('house', models.ForeignKey(to='hotelBooking.House', verbose_name='房型', related_name='house_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HousePackage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('need_point', models.IntegerField(verbose_name='所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='前台现付价格')),
                ('package_state', models.CharField(default='充沛', choices=[('1', '充沛'), ('2', '满房')], max_length=255)),
                ('detail', models.TextField()),
                ('house', models.ForeignKey(to='hotelBooking.House', verbose_name='房型', related_name='housePackages')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(default=django.utils.timezone.now, max_length=200)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', default=['public', 'private'], null=True)),
                ('deviceToken', models.CharField(null=True, max_length=200)),
                ('deviceType', models.CharField(default='android', max_length=200)),
                ('installationId', models.CharField(verbose_name='设备id', null=True, max_length=200)),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='绑定用户', null=True)),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.IntegerField(serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('identifier', hotelBooking.core.fields.InternalIdentifierField(editable=False, db_index=True, max_length=64, blank=True, unique=True, null=True)),
                ('label', models.CharField(verbose_name='label', max_length=32, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('number', models.CharField(unique=True, blank=True, max_length=30, db_index=True, null=True)),
                ('reference_number', models.CharField(db_index=True, max_length=64, verbose_name='reference number', blank=True, unique=True, null=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', default=False, db_index=True)),
                ('payment_status', enumfields.fields.EnumIntegerField(enum=hotelBooking.core.models.orders.PaymentStatus, verbose_name='payment status', default=1, db_index=True)),
                ('shipping_status', enumfields.fields.EnumIntegerField(enum=hotelBooking.core.models.orders.ShippingStatus, verbose_name='shipping status', default=0, db_index=True)),
                ('customer', models.ForeignKey(to='hotelBooking.CustomerMember', on_delete=django.db.models.deletion.PROTECT, verbose_name='customer', blank=True, null=True, related_name='customer_orders')),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, verbose_name='modifier user', blank=True, null=True, related_name='orders_modified')),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('created_on',),
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', default=False, editable=False, db_index=True)),
                ('shipping_mode', enumfields.fields.EnumIntegerField(verbose_name='shipping mode', default=0, enum=hotelBooking.core.models.products.ShippingMode)),
                ('owner', models.ForeignKey(to='hotelBooking.FranchiseeMember')),
            ],
            options={
                'verbose_name': '产品（数据库基类）',
                'ordering': ('-id',),
                'verbose_name_plural': '产品（数据库基类）',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('identifier', models.IntegerField(unique=True)),
                ('name', models.CharField(verbose_name='name', max_length=64)),
            ],
            options={
                'verbose_name': '产品类型',
                'verbose_name_plural': '产品类型',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_py', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(to='hotelBooking.ProductType', verbose_name='product type'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='hotelBooking.Product', on_delete=django.db.models.deletion.PROTECT, verbose_name='product', blank=True, null=True, related_name='product_orders'),
        ),
        migrations.AddField(
            model_name='housepackage',
            name='product',
            field=models.OneToOneField(to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='order',
            field=models.OneToOneField(to='hotelBooking.Order'),
        ),
        migrations.AddField(
            model_name='hotelpackageorder',
            name='snapshot',
            field=models.ForeignKey(to='hotelBooking.HotelPackgeOrderSnapShot', blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='hotelBooking.Province', verbose_name='所属省份', related_name='citys'),
        ),
    ]
