# Generated by Django 3.1.5 on 2021-03-23 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20210323_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='rentDays',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='rentHours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
