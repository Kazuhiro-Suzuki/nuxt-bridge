# Generated by Django 4.2.5 on 2023-10-17 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20231017_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='segment_age_range',
            field=models.JSONField(blank=True, default=list, null=True, verbose_name='セグメント配信-年齢範囲'),
        ),
    ]