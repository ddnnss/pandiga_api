# Generated by Django 3.0.8 on 2020-09-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200823_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='isUnread',
            field=models.BooleanField(default=False, verbose_name='Не прочитанное сообщение'),
        ),
    ]
