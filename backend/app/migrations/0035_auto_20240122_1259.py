# Generated by Django 4.2.5 on 2024-01-22 12:59

from django.db import migrations

from psqlextra.backend.migrations.operations import PostgresAddListPartition

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_facilitylistregionsetting_list_cash'),
    ]

    operations = [
        PostgresAddListPartition(
           model_name="PartitionedInquiry",
           name="region_69",
           values=[69],
        ),
        PostgresAddListPartition(
           model_name="PartitionedMirairoUserConnection",
           name="region_69",
           values=[69],
        ),
        PostgresAddListPartition(
           model_name="PartitionedMirairoUserCertificate",
           name="region_69",
           values=[69],
        ),
        PostgresAddListPartition(
           model_name="PartitionedFirebaseToken",
           name="region_69",
           values=[69],
        ),
    ]
