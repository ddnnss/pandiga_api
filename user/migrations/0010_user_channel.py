# Generated by Django 3.0.8 on 2020-09-16 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20200915_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='channel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]