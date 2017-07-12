# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import model_utils.fields
import django.utils.timezone
import jsonfield.fields
import chaolife.models.fields
import common.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.CharField(primary_key=True, verbose_name='城市代号', serialize=False, unique=True, max_length=40)),
                ('name', models.CharField(db_index=True, verbose_name='城市', unique=True, max_length=200)),
                ('hot', models.IntegerField(default=0, help_text='热门度')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('modified', models.DateTimeField(verbose_name='State modified', auto_now_add=True)),
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(verbose_name='酒店名', max_length=200)),
                ('english_name', models.CharField(blank=True, verbose_name='英文名称', null=True, max_length=255)),
                ('smoking', models.BooleanField(default=True, verbose_name='can smoke ')),
                ('address', models.CharField(verbose_name='地址', max_length=255)),
                ('introduce', models.TextField(verbose_name='介绍', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='联系电话', max_length=255)),
                ('cover_img', models.ImageField(verbose_name='封面图片', upload_to='')),
                ('agent', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(verbose_name='所在城市', null=True, related_name='hotels', to='chaolife.City', on_delete=django.db.models.deletion.SET_NULL)),
                ('type', models.ForeignKey(to='hotel.HotelType', blank=True)),
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
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('hotel', models.ForeignKey(verbose_name='房型', related_name='hotel_imgs', to='chaolife.Hotel')),
            ],
            options={
                'verbose_name': '房间展示图片',
            },
        ),
        migrations.CreateModel(
            name='HotelOrderCreditCardModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('credit_card_type', models.CharField(blank=True, validators=[common.models.validate_card_type], max_length=10)),
                ('credit_card_number', models.CharField(blank=True, max_length=30)),
                ('credit_card_validity_date', models.DateField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='HotelOrderNumberGenerator',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('last_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('number', models.CharField(db_index=True, unique=True, max_length=64, primary_key=True, blank=True, serialize=False, editable=False)),
                ('deleted', models.BooleanField(default=False, db_index=True, verbose_name='deleted')),
                ('payment_status', models.IntegerField(default=1, db_index=True, verbose_name='payment status', choices=[(0, 'not paid'), (1, 'partially paid'), (2, 'fully paid'), (3, 'canceled '), (4, 'deferred')])),
                ('shipping_status', models.IntegerField(default=0, db_index=True, verbose_name='shipping status', choices=[(0, 'not shipped'), (1, 'not shipped'), (2, 'fully shipped')])),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('modified',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('product_name', models.CharField(help_text='Product name at the moment of purchase', blank=True, verbose_name='Product name', null=True, max_length=255)),
                ('product_code', models.CharField(help_text='Product default_code at the moment of purchase', blank=True, verbose_name='Product default_code ', null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('checked', models.BooleanField(default=False, verbose_name='审核通过')),
                ('deleted', models.BooleanField(default=False, verbose_name='已删除 ?')),
                ('active', models.BooleanField(default=False, verbose_name='已上线 ?')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('type', models.IntegerField(default=1, verbose_name='product type', editable=False, choices=[(1, '酒店订房')])),
            ],
            options={
                'verbose_name': '产品（数据库基类）',
                'verbose_name_plural': '产品（数据库基类）',
                'ordering': ('-id',),
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
                ('checked', models.BooleanField(default=False, verbose_name='审核通过')),
                ('deleted', models.BooleanField(default=False, verbose_name='已删除 ?')),
                ('active', models.BooleanField(default=False, verbose_name='已上线 ?')),
                ('id', models.AutoField(primary_key=True, serialize=False, editable=False)),
                ('name', models.CharField(default='未定义房型名', verbose_name='房型', max_length=255)),
                ('hotel', models.ForeignKey(verbose_name='所属酒店', related_name='hotel_rooms', to='chaolife.Hotel')),
            ],
            options={
                'verbose_name': '房型',
                'verbose_name_plural': '房型',
            },
        ),
        migrations.CreateModel(
            name='RoomDayState',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('s_point', models.PositiveIntegerField(default=0, verbose_name='当天单人所需积分')),
                ('s_price', models.PositiveIntegerField(verbose_name='当天单人前台现付价格')),
                ('d_point', models.PositiveIntegerField(default=0, verbose_name='当天双人所需积分')),
                ('d_price', models.PositiveIntegerField(verbose_name='当天双人前台现付价格')),
                ('date', models.DateField()),
                ('state', models.IntegerField(default=1, choices=[(1, '尚还有房'), (0, '没有房了')])),
                ('agent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(to='chaolife.City', related_name='roomstates')),
                ('hotel', models.ForeignKey(to='chaolife.Hotel', related_name='roomstates')),
                ('room', models.ForeignKey(to='chaolife.Room')),
            ],
            options={
                'verbose_name': '房间类型状态',
                'verbose_name_plural': '房间类型状态',
                'get_latest_by': 'date',
                'ordering': ('agent', 'date'),
            },
        ),
        migrations.CreateModel(
            name='RoomImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(verbose_name='图片', upload_to='')),
                ('room', models.ForeignKey(verbose_name='房型', related_name='room_imgs', to='chaolife.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelPackageOrder',
            fields=[
                ('order_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='chaolife.Order')),
                ('checkin_time', models.DateField(db_index=True, verbose_name='入住时间')),
                ('latest_checkin_hour', chaolife.models.fields.HourField(default='14:00', verbose_name='最晚到店时间', choices=[('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00'), ('24:00', '24:00')], max_length=255)),
                ('checkout_time', models.DateField(db_index=True, verbose_name='离店时间')),
                ('process_state', models.IntegerField(default=1, db_index=True, help_text='订单进行的状态', choices=[(1, '客户已经发起请求'), (2, '客户取消了入住'), (3, '客户暂未入住，提前表示不能入住'), (11, '代理接收了订单,但是用户尚未入住'), (12, '代理拒绝了订单'), (13, '代理提前表示某些原因导致不能入住了'), (-100, '代理超时确认，自动取消'), (20, '交易成功，时间到入住时间了(通常是在checkoutTime之后标记为此状态)'), (30, '到达ckeckoutTime之后，将订单')])),
                ('closed', models.BooleanField(default=False)),
                ('success', models.BooleanField(default=False, help_text='交易正常，用户正常入住')),
                ('point_flow_to_seller', models.BooleanField(default=False, help_text='积分是否已经转到代理商账号(前提是 success = True)')),
                ('point_flow_to_seller_count', models.FloatField(default=0, help_text='积分转到代理商账号的数量')),
                ('point_refund_to_customer_count', models.IntegerField(default=0, help_text='积分退还给用户的数量')),
                ('process_state_change_at', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='process_state')),
                ('total_front_prices', models.IntegerField(verbose_name='total need prices', help_text='所需前台总价')),
                ('total_need_points', models.IntegerField(verbose_name='total need points', help_text='所需积分总和')),
                ('breakfast', models.IntegerField(default=1, verbose_name='早餐类型', help_text=' 订单生成时,所记录的早餐类型')),
                ('hotel_name', models.CharField(verbose_name='hotel name', help_text='hotel name at the moment of purchase', max_length=255)),
                ('hotel_address', models.CharField(verbose_name='hotel address', help_text='酒店地址', max_length=500)),
                ('room_name', models.CharField(verbose_name='room name', help_text='room name at the moment of purchase', max_length=255)),
                ('request_remark', models.CharField(help_text='用户订单要求', blank=True, null=True, max_length=500)),
                ('room_count', models.SmallIntegerField(default=1, verbose_name='房间件数')),
                ('people_count', models.SmallIntegerField(default=1, verbose_name='入住人数')),
                ('comment', models.CharField(help_text='消费评价', blank=True, null=True, max_length=500)),
                ('guests', jsonfield.fields.JSONField(blank=True, null=True, help_text='入住人信息')),
            ],
            options={
                'permissions': (('change_process_state', '能够操作改变订单过程状态'),),
                'ordering': ('-process_state_change_at',),
            },
            bases=('chaolife.order',),
        ),
        migrations.CreateModel(
            name='HotelPackageOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='chaolife.OrderItem')),
                ('day', models.DateField(verbose_name='check in day', help_text='日期')),
                ('point', models.IntegerField(verbose_name='need point', help_text='所需积分(moment)')),
                ('price', models.IntegerField(verbose_name='front price', help_text='当天前台现付价格(moment)')),
            ],
            bases=('chaolife.orderitem',),
        ),
        migrations.CreateModel(
            name='RoomPackage',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to='chaolife.Product')),
                ('hotel_name', models.CharField(verbose_name='酒店名', max_length=254)),
                ('room_name', models.CharField(verbose_name='房型名', max_length=254)),
                ('breakfast', models.IntegerField(default=1, verbose_name='早餐类型', choices=[(1, '无早'), (2, '单早'), (3, '双早')])),
                ('bill', models.BooleanField(default=True, verbose_name='提供发票')),
                ('smoking', models.BooleanField(default=True, verbose_name='有烟?', help_text='0 表示 无烟房,1表示没有明确表示')),
                ('price_type', models.IntegerField(default=1, verbose_name='价格类型', choices=[(1, '单双同价'), (2, '单双异价')])),
                ('default_s_point', models.PositiveIntegerField(default=0, verbose_name='默认单人所需积分')),
                ('default_s_price', models.PositiveIntegerField(verbose_name='默认单人现付价格')),
                ('default_d_point', models.PositiveIntegerField(default=0, verbose_name='默认双人所需积分')),
                ('default_d_price', models.PositiveIntegerField(verbose_name='默认双人现付价格')),
                ('extra', jsonfield.fields.JSONField(blank=True, verbose_name='Extra fields', null=True, help_text='Arbitrary information for this roompackage object.')),
                ('hotel', models.ForeignKey(verbose_name='酒店', to='chaolife.Hotel')),
                ('room', models.ForeignKey(verbose_name='房型', related_name='roomPackages', to='chaolife.Room')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
            },
            bases=('chaolife.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(verbose_name='Order', related_name='items', to='chaolife.Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(verbose_name='Product', null=True, blank=True, to='chaolife.Product', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', related_name='customer_orders', blank=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='modified_by',
            field=models.ForeignKey(verbose_name='modifier user', null=True, related_name='orders_modified', blank=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name='product', null=True, related_name='product_orders', blank=True, to='chaolife.Product', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(default=1000, related_name='seller_orders', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(verbose_name='所属省份', null=True, related_name='citys', blank=True, to='chaolife.Province'),
        ),
        migrations.AddField(
            model_name='roomdaystate',
            name='roomPackage',
            field=models.ForeignKey(to='chaolife.RoomPackage', related_name='roomstates'),
        ),
        migrations.AddField(
            model_name='hotelordercreditcardmodel',
            name='order',
            field=models.OneToOneField(to='chaolife.HotelPackageOrder'),
        ),
        migrations.CreateModel(
            name='ClosedHotelPackageOrder',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('chaolife.hotelpackageorder',),
        ),
    ]
