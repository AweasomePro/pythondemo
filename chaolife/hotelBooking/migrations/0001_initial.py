# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotelBooking.utils.fiels
import jsonfield.fields
import hotelBooking.core.fields.pointField
import hotelBooking.models.counters
import django.db.models.deletion
import model_utils.fields
from django.conf import settings
import uuid
import enumfields.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20160712_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=225, default='unknow name')),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('sex', models.IntegerField(choices=[(1, 'male'), (0, 'female')], default=1)),
                ('phone_is_verify', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_loggin', models.BooleanField(default=False)),
                ('role', models.IntegerField(choices=[(1, '顾客'), (2, '酒店代理合作伙伴')], help_text='该账号的角色标识', default=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('point', hotelBooking.core.fields.pointField.PointField(verbose_name='积分', default=0, editable=False)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.IntegerField(verbose_name='城市代号', serialize=False, unique=True, primary_key=True)),
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
                ('id', enumfields.fields.EnumIntegerField(verbose_name='identifier', serialize=False, enum=hotelBooking.models.counters.CounterType, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('smoking', models.BooleanField(verbose_name='can smoke ', default=False)),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
                ('cover_img', models.ImageField(verbose_name='封面图片', upload_to='')),
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
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('hotel', models.ForeignKey(related_name='hotel_imgs', verbose_name='房型', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name': '房间展示图片',
            },
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valid', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=200, default=django.utils.timezone.now)),
                ('channels', hotelBooking.utils.fiels.ListField(verbose_name='订阅渠道', null=True, default=['public', 'private'])),
                ('deviceToken', models.CharField(null=True, max_length=200)),
                ('installationId', models.CharField(verbose_name='设备id', null=True, max_length=200)),
                ('deviceType', models.CharField(max_length=200, default='android')),
                ('badge', models.BigIntegerField(verbose_name='ios badge数', default=0)),
                ('deviceProfile', models.CharField(max_length=200, default='')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_list', hotelBooking.utils.fiels.ListField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('number', models.CharField(serialize=False, max_length=64, unique=True, blank=True, primary_key=True, db_index=True, editable=False)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False)),
                ('payment_status', models.IntegerField(verbose_name='payment status', choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')], db_index=True, default=1)),
                ('shipping_status', models.IntegerField(verbose_name='shipping status', choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')], db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'order',
                'ordering': ('modified',),
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(verbose_name='Product name', null=True, max_length=255, help_text='Product name at the moment of purchase', blank=True)),
                ('product_code', models.CharField(verbose_name='Product default_code ', null=True, max_length=255, help_text='Product default_code at the moment of purchase', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('trade_no', models.CharField(max_length=32, db_index=True, editable=False)),
                ('unit_price', models.PositiveIntegerField(verbose_name='单位价格(元)', default=1)),
                ('number', models.PositiveIntegerField(verbose_name='购买的数量')),
                ('total_price', models.FloatField(verbose_name='总价')),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1)),
                ('pay_method', models.IntegerField(choices=[(1, '支付宝')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(verbose_name='create on', auto_now_add=True)),
                ('modified_on', models.DateTimeField(verbose_name='modified on', auto_now=True)),
                ('deleted', models.BooleanField(verbose_name='deleted', db_index=True, default=False, editable=False)),
                ('type', models.IntegerField(verbose_name='product type', choices=[(1, '酒店订房')], default=1, editable=False)),
            ],
            options={
                'verbose_name': '产品（数据库基类）',
                'ordering': ('-id',),
                'verbose_name_plural': '产品（数据库基类）',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(verbose_name='房型', max_length=255, default='未定义房型名')),
                ('hotel', models.ForeignKey(related_name='hotel_rooms', verbose_name='所属酒店', to='hotelBooking.Hotel')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='RoomDayState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('s_point', models.PositiveIntegerField(verbose_name='当天单人所需积分', default=0)),
                ('s_price', models.PositiveIntegerField(verbose_name='当天单人前台现付价格')),
                ('d_point', models.PositiveIntegerField(verbose_name='当天双人所需积分', default=0)),
                ('d_price', models.PositiveIntegerField(verbose_name='当天双人前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(choices=[(1, 'room is enough'), (2, 'room is few'), (3, 'room has no empty')], default=1)),
            ],
            options={
                'verbose_name': '房间类型状态',
                'ordering': ('agent', 'date'),
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('room', models.ForeignKey(related_name='room_imgs', verbose_name='房型', to='hotelBooking.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMember',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
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
                ('order', models.OneToOneField(serialize=False, to='hotelBooking.Order', primary_key=True)),
                ('checkin_time', models.DateField(verbose_name='入住时间')),
                ('checkout_time', models.DateField(verbose_name='离店时间')),
                ('closed', models.BooleanField(default=False)),
                ('process_state', models.IntegerField(choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了')], help_text='订单进行的状态', default=1)),
                ('total_front_prices', models.IntegerField(verbose_name='total need prices', help_text='所需前台总价')),
                ('total_need_points', models.IntegerField(verbose_name='total need points', help_text='所需积分总和')),
                ('breakfast', models.IntegerField(verbose_name='早餐类型', help_text=' 订单生成时,所记录的早餐类型', default=1)),
                ('hotel_name', models.CharField(verbose_name='hotel name', max_length=255, help_text='hotel name at the moment of purchase')),
                ('room_name', models.CharField(verbose_name='room name', max_length=255, help_text='room name at the moment of purchase')),
                ('request_notes', models.TextField(null=True, help_text='用户订单要求', blank=True)),
                ('room_count', models.SmallIntegerField(verbose_name='房间件数', default=1)),
                ('people_count', models.SmallIntegerField(verbose_name='入住人数', default=1)),
                ('comment', models.TextField(null=True, help_text='消费评价', blank=True)),
                ('guests', jsonfield.fields.JSONField(null=True, help_text='入住人信息', blank=True)),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
            },
            bases=('hotelBooking.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(serialize=False, parent_link=True, to='hotelBooking.OrderItem', auto_created=True, primary_key=True)),
                ('day', models.DateField(verbose_name='check in day', help_text='日期')),
                ('point', models.IntegerField(verbose_name='need point', help_text='所需积分(moment)')),
                ('price', models.IntegerField(verbose_name='front price', help_text='当天前台现付价格(moment)')),
            ],
            bases=('hotelBooking.orderitem',),
        ),
        migrations.CreateModel(
            name='PartnerMember',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
            ],
            options={
                'verbose_name': '加盟会员',
                'verbose_name_plural': '加盟会员',
            },
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(serialize=False, parent_link=True, to='hotelBooking.Product', auto_created=True, primary_key=True)),
                ('checked', models.BooleanField(verbose_name='审核过 ?', default=False)),
                ('active', models.BooleanField(verbose_name='是否可用 ?', default=False)),
                ('breakfast', models.IntegerField(verbose_name='早餐类型', choices=[(1, '无早'), (2, '单早'), (3, '双早')], default=1)),
                ('bill', models.BooleanField(verbose_name='提供发票', default=True)),
                ('price_type', models.IntegerField(verbose_name='价格类型', choices=[(1, '单双同价'), (2, '单双异价')], default=1)),
                ('default_s_point', models.PositiveIntegerField(verbose_name='默认单人所需积分', default=0)),
                ('default_s_price', models.PositiveIntegerField(verbose_name='默认单人现付价格')),
                ('default_d_point', models.PositiveIntegerField(verbose_name='默认双人所需积分', default=0)),
                ('default_d_price', models.PositiveIntegerField(verbose_name='默认双人现付价格')),
                ('extra', jsonfield.fields.JSONField(verbose_name='Extra fields', null=True, help_text='Arbitrary information for this roompackage object.', blank=True)),
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
            field=models.ForeignKey(related_name='items', verbose_name='Order', to='hotelBooking.Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, verbose_name='Product', to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, related_name='customer_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(null=True, related_name='orders_modified', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='modifier user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, related_name='product_orders', on_delete=django.db.models.deletion.PROTECT, verbose_name='product', to='hotelBooking.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, related_name='seller_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='installation',
            name='user',
            field=models.ForeignKey(null=True, to_field='phone_number', verbose_name='绑定用户', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotel',
            name='agent',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(related_name='hotels', verbose_name='所在城市', to='hotelBooking.City'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(related_name='citys', verbose_name='所属省份', to='hotelBooking.Province'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='groups', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='user permissions', to='auth.Permission', help_text='Specific permissions for this user.', related_query_name='user'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='hotel',
            field=models.ForeignKey(verbose_name='酒店', to='hotelBooking.Hotel'),
        ),
        migrations.AddField(
            model_name='roompackage',
            name='room',
            field=models.ForeignKey(related_name='roomPackages', verbose_name='房型', to='hotelBooking.Room'),
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
