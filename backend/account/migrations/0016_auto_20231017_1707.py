# Generated by Django 4.2.5 on 2023-10-17 17:07

from django.db import migrations

from psqlextra.backend.migrations.operations import PostgresAddListPartition

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_remove_partitioneduserprofile_list_disability_category_and_more'),
    ]

    operations = [
        PostgresAddListPartition(
           model_name="PartitionedUserProfile",
           name="region_68",
           values=[68],
       ),
       PostgresAddListPartition(
           model_name="PartitionedUserCityCa",
           name="region_68",
           values=[68],
        ),
        PostgresAddListPartition(
           model_name="PartitionedResetPassword",
           name="region_68",
           values=[68],
        ),
        PostgresAddListPartition(
           model_name="FacilityManger",
           name="region_68",
           values=[68],
        ),   
    ]