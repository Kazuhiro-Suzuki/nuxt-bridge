# Generated by Django 4.2.5 on 2024-02-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20240206_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='segment_birthday_year',
            field=models.JSONField(blank=True, default=list, null=True, verbose_name='セグメント配信-誕生年'),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='category',
            field=models.CharField(choices=[('app', '本アプリの活用方法'), ('notification', 'お知らせ内容'), ('registration', '会員登録'), ('mirairo', 'ミライロID'), ('reservation', '短期入所施設予約'), ('reserve_consult', 'オンライン相談予約'), ('support_file', 'るぴなすノート'), ('other', 'ご意見、その他')], default='other', max_length=32),
        ),
        migrations.AlterField(
            model_name='partitionedinquiry',
            name='category',
            field=models.CharField(choices=[('app', '本アプリの活用方法'), ('notification', 'お知らせ内容'), ('registration', '会員登録'), ('mirairo', 'ミライロID'), ('reservation', '短期入所施設予約'), ('reserve_consult', 'オンライン相談予約'), ('support_file', 'るぴなすノート'), ('other', 'ご意見、その他')], default='other', max_length=32),
        ),
    ]
