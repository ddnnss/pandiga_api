# Generated by Django 3.0.8 on 2020-10-29 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20201011_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refferal',
            name='earned',
            field=models.IntegerField(default=0, verbose_name='Начислено'),
        ),
    ]