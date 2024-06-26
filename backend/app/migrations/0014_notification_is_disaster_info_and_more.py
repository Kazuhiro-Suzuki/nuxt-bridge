# Generated by Django 4.0.3 on 2022-11-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_region_department_region_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_disaster_info',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='segment_address_block',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='segment_birthday',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='segment_disability_type',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='segment_user_type',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
