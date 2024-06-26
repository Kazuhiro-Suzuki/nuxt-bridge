# Generated by Django 4.0.3 on 2022-09-29 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import psqlextra.backend.migrations.operations.add_default_partition
import psqlextra.backend.migrations.operations.create_partitioned_model
import psqlextra.manager.manager
import psqlextra.models.partitioned
import psqlextra.types
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20220929_1733'),
        ('account', '0002_user_is_subscribe'),
    ]

    operations = [
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name='PartitionedResetPassword',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expiration_at', models.DateTimeField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region')),
            ],
            options={
                'verbose_name_plural': 'パスワード変更 - パーティション',
                'managed': True,
            },
            partitioning_options={
                'method': psqlextra.types.PostgresPartitioningMethod['LIST'],
                'key': ['region_id'],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name='PartitionedResetPassword',
            name='default',
        ),
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name='PartitionedUserCityCa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=512)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region')),
            ],
            options={
                'verbose_name_plural': 'CityCaユーザ - パーティション',
                'managed': True,
            },
            partitioning_options={
                'method': psqlextra.types.PostgresPartitioningMethod['LIST'],
                'key': ['region_id'],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name='PartitionedUserCityCa',
            name='default',
        ),
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name='PartitionedUserProfile',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('kana_last_name', models.CharField(blank=True, max_length=45, null=True, verbose_name='姓（フリガナ）')),
                ('kana_first_name', models.CharField(blank=True, max_length=45, null=True, verbose_name='名（フリガナ）')),
                ('last_name', models.CharField(blank=True, max_length=45, null=True, verbose_name='姓（漢字）')),
                ('first_name', models.CharField(blank=True, max_length=45, null=True, verbose_name='名（漢字）')),
                ('phone_number', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=32, null=True)),
                ('user_type', models.CharField(blank=True, choices=[('person', '本人'), ('family', '家族'), ('caregiver', '介助者'), ('other', 'その他')], max_length=50, null=True)),
                ('account_type', models.CharField(choices=[('general', 'general_user'), ('business', 'business_user'), ('facility', 'facility_user')], default='general', max_length=16)),
                ('birthday_year', models.CharField(blank=True, max_length=2, null=True, verbose_name='生年月日-年')),
                ('birthday_month', models.CharField(blank=True, max_length=2, null=True, verbose_name='生年月日-月')),
                ('birthday_day', models.CharField(blank=True, max_length=2, null=True, verbose_name='生年月日-日')),
                ('postal_code_1', models.CharField(blank=True, max_length=3, null=True, verbose_name='郵便番号-上3桁')),
                ('postal_code_2', models.CharField(blank=True, max_length=4, null=True, verbose_name='郵便番号-下4桁')),
                ('address_prefecture', models.CharField(blank=True, max_length=10, null=True, verbose_name='都道府県')),
                ('address_city', models.CharField(blank=True, max_length=20, null=True, verbose_name='市区町村')),
                ('address_block', models.CharField(blank=True, max_length=50, null=True, verbose_name='番地')),
                ('disability_type', models.CharField(blank=True, choices=[('mental', '精神通院'), ('incurable', '難病'), ('other', 'その他')], max_length=50, null=True, verbose_name='障がい種別（3手帳）')),
                ('is_subscribe', models.BooleanField(default=True, verbose_name='メール配信-有効')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region')),
            ],
            options={
                'verbose_name_plural': 'ユーザプロファイル',
            },
            partitioning_options={
                'method': psqlextra.types.PostgresPartitioningMethod['LIST'],
                'key': ['region_id'],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name='PartitionedUserProfile',
            name='default',
        ),
        migrations.AddField(
            model_name='resetpassword',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region'),
        ),
        migrations.AddField(
            model_name='usercityca',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.region'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=32),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partitionedusercityca',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partitionedresetpassword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='partitioneduserprofile',
            constraint=models.UniqueConstraint(fields=('user_id', 'region_id'), name='unique_for_user_profile'),
        ),
        migrations.AddConstraint(
            model_name='partitionedusercityca',
            constraint=models.UniqueConstraint(fields=('user_id', 'region_id'), name='unique_for_user_city_ca'),
        ),
    ]
