# Generated by Django 4.2.6 on 2023-11-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_payment_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(max_length=100, verbose_name='Способ оплаты'),
        ),
    ]