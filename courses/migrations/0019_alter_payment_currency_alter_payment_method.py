# Generated by Django 4.2.6 on 2023-11-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_alter_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='usd', max_length=50, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(default='card', max_length=100, verbose_name='Способ оплаты'),
        ),
    ]
