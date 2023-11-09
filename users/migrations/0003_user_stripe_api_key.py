# Generated by Django 4.2.6 on 2023-11-09 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_api_key',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Stripe API-key'),
        ),
    ]
