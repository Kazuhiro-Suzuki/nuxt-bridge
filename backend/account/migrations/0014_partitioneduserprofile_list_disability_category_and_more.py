# Generated by Django 4.0.3 on 2023-06-23 19:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20230623_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='list_disability_category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, default=list, null=True, size=None, verbose_name='障がいカテゴリー'),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='note1',
            field=models.TextField(blank=True, null=True, verbose_name='備考1'),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='note2',
            field=models.TextField(blank=True, null=True, verbose_name='備考2'),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='note3',
            field=models.TextField(blank=True, null=True, verbose_name='備考3'),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='notification_tag',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, default=list, null=True, size=None, verbose_name='お知らせ配信のタグ'),
        ),
        migrations.AddField(
            model_name='partitioneduserprofile',
            name='user_type_detail',
            field=models.TextField(blank=True, null=True, verbose_name='障がい児者との関係の詳細'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='disability_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, default=list, null=True, size=None, verbose_name='障がい種別'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='fax_number',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='ファックス番号'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='get_disaster_notification',
            field=models.BooleanField(default=True, verbose_name='災害時のお知らせ通知を有効にする'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='get_notification',
            field=models.BooleanField(default=True, verbose_name='通常のお知らせ通知を有効にする'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='is_dangerous',
            field=models.BooleanField(default=False, verbose_name='要注意人物を有効にする'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='is_subscribe',
            field=models.BooleanField(default=True, verbose_name='メール配信を有効にする'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='電話番号'),
        ),
        migrations.AlterField(
            model_name='partitioneduserprofile',
            name='user_type',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='障がい児者との関係'),
        ),
    ]