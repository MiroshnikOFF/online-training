# Generated by Django 4.2.6 on 2023-11-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_alter_payment_currency_alter_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(max_length=50, verbose_name='Валюта'),
        ),
    ]