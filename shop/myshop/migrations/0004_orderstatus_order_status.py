# Generated by Django 5.1.4 on 2024-12-30 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0003_alter_courier_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('in_progress', 'В работе менеджера'), ('confirmed', 'Подтвержден'), ('assembling', 'В сборке'), ('in_delivery', 'В доставке'), ('completed', 'Завершен')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Статус заказа',
                'verbose_name_plural': 'Статусы заказов',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myshop.orderstatus'),
        ),
    ]
