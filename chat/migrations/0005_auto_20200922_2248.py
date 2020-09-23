# Generated by Django 3.0.8 on 2020-09-22 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20200922_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='starter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='isUnread',
            field=models.BooleanField(default=True, verbose_name='Не прочитанное сообщение'),
        ),
    ]