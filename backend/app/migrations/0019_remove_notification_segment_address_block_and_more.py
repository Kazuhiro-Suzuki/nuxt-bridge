# Generated by Django 4.0.3 on 2022-12-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_notificationconnection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='segment_address_block',
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='category',
            field=models.CharField(choices=[('app', '本アプリの活用方法'), ('notification', 'お知らせ内容'), ('registration', '会員登録'), ('mirairo', 'ミライロID'), ('reservation', '短期入所施設予約'), ('reserve_consult', 'オンライン相談予約'), ('other', 'ご意見、その他')], default='other', max_length=32),
        ),
        migrations.AlterField(
            model_name='partitionedinquiry',
            name='category',
            field=models.CharField(choices=[('app', '本アプリの活用方法'), ('notification', 'お知らせ内容'), ('registration', '会員登録'), ('mirairo', 'ミライロID'), ('reservation', '短期入所施設予約'), ('reserve_consult', 'オンライン相談予約'), ('other', 'ご意見、その他')], default='other', max_length=32),
        ),
    ]
