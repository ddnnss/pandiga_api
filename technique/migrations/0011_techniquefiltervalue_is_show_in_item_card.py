# Generated by Django 3.0.8 on 2020-08-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0010_auto_20200806_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='techniquefiltervalue',
            name='is_show_in_item_card',
            field=models.BooleanField(default=False),
        ),
    ]
