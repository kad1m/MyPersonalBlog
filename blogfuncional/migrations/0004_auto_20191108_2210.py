# Generated by Django 2.2.6 on 2019-11-08 20:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogfuncional', '0003_auto_20191108_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 8, 20, 10, 41, 390508, tzinfo=utc)),
        ),
    ]