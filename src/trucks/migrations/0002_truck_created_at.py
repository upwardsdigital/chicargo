# Generated by Django 4.2.1 on 2023-05-16 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 16, 9, 15, 48, 216499)),
        ),
    ]
