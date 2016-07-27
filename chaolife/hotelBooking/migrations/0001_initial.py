# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
from django.conf import settings
import hotelBooking.core.fields.pointField
import enumfields.fields
import hotelBooking.models.counters
import django.db.models.deletion
import django.utils.timezone
import hotelBooking.utils.fiels
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('phone_number', models.CharField(unique=True, max_length=15)),
                ('name', models.CharField(default='unknow name', max_length=225)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('sex', models.IntegerField(choices=[(1, 'male'), (0, 'female')], default=1)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('role', models.IntegerField(help_text='该账号的角色标识', default=1, choices=[(1, '顾客'), (2, '酒店代理合作伙伴')])),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(verbose_name='积分', editable=False, default=0)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='城市代号')),
                ('name', models.CharField(verbose_name='城市', max_length=200)),
                ('logo', models.URLField(verbose_name='城市Logo图', default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', enumfields.fields.EnumIntegerField(primary_key=True, serialize=False, verbose_name='identifier', enum=hotelBooking.models.counters.CounterType)),
                ('value', models.IntegerField(verbose_name='value', default=0)),
            ],
            options={
                'verbose_name': 'counter',
                'verbose_name_plural': 'counters',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('active', models.BooleanField(verbose_name='是否可用', default=True)),
                ('modified', models.DateTimeField(verbose_name='State modified', auto_now_add=True)),
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
            ],
            options={
                'verbose_name': '酒店',
                'verbose_name_plural': '酒店',
            },
        ),
        migrations.CreateModel(
            name='HotelImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('hotel', models.ForeignKey(verbose_name='房型', to='hotelBooking.Hotel', related_name='hotel_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(default=django.utils.timezone.now, max_length=200)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', default=['public', 'private'], null=True)),
                ('deviceToken', models.CharField(null=True, max_length=200)),
                ('installationId', models.CharField(verbose_name='设备id', null=True, max_length=200)),
                ('deviceType', models.CharField(default='android', max_length=200)),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(default='', max_length=200)),
                ('active', models.BooleanField(verbose_name='active?', default=True)),
            ],
            options={
                'verbose_name': 'App已安装设备',
                'verbose_name_plural': '设备',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('number', models.CharField(serialize=False, unique=True, primary_key=True, db_index=True, blank=True, max_length=30)),
                ('created_on', models.DateTimeField(verbose_name='created on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now_add=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False)),
                ('payment_status', models.IntegerField(choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], db_index=True, default=1, verbose_name='payment status')),
                ('shipping_status', models.IntegerField(choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], db_index=True, default=0, verbose_name='shipping status')),
            ],
            options={
                'ordering': ('created_on',),
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(help_text='Product name at the moment of purchase', null=True, verbose_name='Product name', blank=True, max_length=255)),
                ('product_code', models.CharField(help_text='Product default_code at the moment of purchase', null=True, verbose_name='Product default_code ', blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('trade_no', models.CharField(editable=False, db_index=True, max_length=32)),
                ('unit_price', models.IntegerField(verbose_name='单位价格(元)', default=1)),
                ('number', models.IntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1)),
                ('pay_method', models.IntegerField(choices=[(1, '支付宝')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', editable=False, db_index=True, default=False)),
                ('type', models.IntegerField(choices=[(1, '酒店订房')], editable=False, default=1, verbose_name='product type')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '产品（数据库基类）',
                'verbose_name_plural': '产品（数据库基类）',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '省份',
                'verbose_name_plural': '省份',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('checked', models.BooleanField(verbose_name='审核过 ?', default=False)),
                ('active', models.BooleanField(verbose_name='是否可用 ?', default=False)),
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(verbose_name='房型', default='未定义房型名', max_length=255)),
                ('hotel', models.ForeignKey(verbose_name='所属酒店', to='hotelBooking.Hotel', related_name='hotel_rooms')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='RoomDayState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_point', models.IntegerField(verbose_name='当天所需积分', default=0)),
                ('front_price', models.IntegerField(verbose_name='当天前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')], default=1)),
            ],
            options={
                'ordering': ('agent', 'date'),
                'verbose_name': '房间类型状态',
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img_url', models.CharField(verbose_name='图片地址', max_length=250)),
                ('room', models.ForeignKey(verbose_name='房型', to='hotelBooking.Room', related_name='room_imgs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('avatar', models.URLField(blank=True)),
                ('last_access', models.DateTimeField(verbose_name='Last accessed', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '会员',
                'verbose_name_plural': '会员',
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order', models.OneToOneField(to='hotelBooking.Order', serialize=False, primary_key=True)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('closed', models.BooleanField(default=False)),
                ('process_state', models.IntegerField(help_text='订单进行的状态', default=1, choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了')])),
                ('total_front_prices', models.IntegerField(help_text='所需前台总价', verbose_name='total need prices')),
                ('total_need_points', models.IntegerField(help_text='所需积分总和', verbose_name='total need points')),
                ('breakfast', models.IntegerField(help_text=' 订单生成时,所记录的早餐类型', default=1, verbose_name='早餐类型')),
                ('hotel_name', models.CharField(help_text='hotel name at the moment of purchase', verbose_name='hotel name', max_length=255)),
                ('room_name', models.CharField(help_text='room name at the moment of purchase', verbose_name='room name', max_length=255)),
                ('request_notes', models.TextField(help_text='用户订单要求', null=True, blank=True)),
                ('comment', models.TextField(help_text='消费评价', null=True, blank=True)),
                ('guests', jsonfield.fields.JSONField(help_text='入住人信息', null=True, blank=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(to='hotelBooking.OrderItem', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('day', models.DateField(help_text='日期', verbose_name='check in day')),
                ('point', models.IntegerField(help_text='所需积分(moment)', verbose_name='need point')),
                ('front_price', models.IntegerField(help_text='当天前台现付价格(moment)', verbose_name='front price')),
            ],
            bases=('hotelBooking.orderitem',),
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(to='hotelBooking.Product', serialize=False, parent_link=True, primary_key=True, auto_created=True)),
                ('checked', models.BooleanField(verbose_name='审核过 ?', default=False)),
                ('active', models.BooleanField(verbose_name='是否可用 ?', default=False)),
                ('breakfast', models.IntegerField(choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1, verbose_name='早餐类型')),
                ('default_point', models.IntegerField(verbose_name='默认所需积分', default=0)),
                ('default_front_price', models.IntegerField(verbose_name='默认前台现付价格')),
                ('extra', jsonfield.fields.JSONField(help_text='Arbitrary information for this roompackage object.', null=True, blank=True, verbose_name='Extra fields')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
            },
            bases=('hotelBooking.product', models.Model),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='agent',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='city',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.City'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='hotel',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.Hotel'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='room',
            field=models.ForeignKey(to='hotelBooking.Room'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pay',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(verbose_name='Order', to='hotelBooking.Order', related_name='items'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(verbose_name='Product', on_delete=django.db.models.deletion.SET_NULL, null=True, to='hotelBooking.Product', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, related_name='customer_orders', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(verbose_name='modifier user', on_delete=django.db.models.deletion.PROTECT, null=True, to=settings.AUTH_USER_MODEL, related_name='orders_modified', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name='product', on_delete=django.db.models.deletion.PROTECT, to='hotelBooking.Product', related_name='product_orders', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='seller_orders', blank=True),
        ),
        migrations.AddField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(verbose_name='绑定用户', null=True, to=settings.AUTH_USER_MODEL, to_field='phone_number'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='agent',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(verbose_name='所在城市', to='hotelBooking.City', related_name='hotels'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', to='hotelBooking.Province', related_name='citys'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set', related_query_name='user', to='auth.Group', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', related_query_name='user', to='auth.Permission', blank=True),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='hotel',
            field=models.ForeignKey(verbose_name='酒店', to='hotelBooking.Hotel'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='room',
            field=models.ForeignKey(verbose_name='房型', to='hotelBooking.Room', related_name='roomPackages'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(related_name='roomstates', to='hotelBooking.RoomPackage'),
        ),
        migrations.CreateModel(
            name='ClosedHotelPackageOrder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('hotelBooking.hotelpackageorder',),
        ),
    ]
