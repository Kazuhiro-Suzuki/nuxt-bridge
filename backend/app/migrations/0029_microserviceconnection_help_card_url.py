# Generated by Django 4.2.5 on 2023-09-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_microserviceconnection'),
    ]

    operations = [
        migrations.AddField(
            model_name='microserviceconnection',
            name='help_card_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='署名付ヘルプカードURL'),
        ),
    ]
