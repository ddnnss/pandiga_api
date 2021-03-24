# Generated by Django 3.1.5 on 2021-03-20 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20201111_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='rentEndTime',
            new_name='rentTime',
        ),
        migrations.RemoveField(
            model_name='order',
            name='rentEndDate',
        ),
        migrations.RemoveField(
            model_name='order',
            name='rentStartDate',
        ),
        migrations.RemoveField(
            model_name='order',
            name='rentStartTime',
        ),
        migrations.AddField(
            model_name='order',
            name='rentDays',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='rentHours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
