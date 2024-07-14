# Generated by Django 5.0.6 on 2024-07-13 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0007_alter_products_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('phone_number', models.CharField(max_length=10, verbose_name='Номер телефона')),
                ('requires_delivery', models.BooleanField(default=False, verbose_name='Требуется доставка')),
                ('delivery_address', models.BooleanField(default=True, verbose_name='Адрес доставки')),
                ('payment_on_get', models.BooleanField(default=False, verbose_name='Оплата при получении')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('status', models.CharField(default='В обработке', max_length=50, verbose_name='Статус заказа')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=7, verbose_name='Стоимость в рублях')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='goods.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'db_table': 'order_item',
            },
        ),
    ]
