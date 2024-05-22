# Generated by Django 4.0.3 on 2023-05-11 13:19

from django.db import migrations

from psqlextra.backend.migrations.operations import PostgresAddListPartition


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20230511_1315'),
    ]

    operations = [
        PostgresAddListPartition(
           model_name="FacilityManger",
           name="region_1",
           values=[1],
        ),
        PostgresAddListPartition(
           model_name="FacilityManger",
           name="region_34",
           values=[34],
        ),
    ]
