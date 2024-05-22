# Generated by Django 3.2.8 on 2024-02-06 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0035_auto_20240122_1259'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='notification',
        #     name='segment_birthday_year',
        #     field=models.JSONField(blank=True, default=list, null=True, verbose_name='セグメント配信-誕生年'),
        # ),
        migrations.CreateModel(
            name='SupportFileRepl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('form_id', models.UUIDField(default=uuid.uuid4)),
                ('repl', models.JSONField(blank=True, default=[], null=True)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'サポートファイル回答',
            },
        ),
        migrations.CreateModel(
            name='SupportFileRegion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.JSONField(blank=True, default=[], null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.region')),
            ],
            options={
                'verbose_name_plural': 'サポートファイル設定',
            },
        ),
        migrations.CreateModel(
            name='SupportFileImg',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('upload_file_key', models.CharField(max_length=511)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'サポートファイル画像ファイル',
            },
        ),
    ]
