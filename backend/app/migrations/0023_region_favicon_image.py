# Generated by Django 4.0.3 on 2023-01-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='favicon_image',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='自治体別ファビコン画像'),
        ),
    ]
