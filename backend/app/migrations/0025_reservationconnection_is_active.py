# Generated by Django 4.0.3 on 2023-06-23 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20230623_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationconnection',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='予約機能を有効にする'),
        ),
    ]
