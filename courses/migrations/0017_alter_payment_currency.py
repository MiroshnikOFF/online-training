# Generated by Django 4.2.6 on 2023-11-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_remove_course_currency_payment_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(max_length=50, verbose_name='Валюта'),
        ),
    ]
