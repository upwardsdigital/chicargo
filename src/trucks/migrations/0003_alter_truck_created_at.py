# Generated by Django 4.2.1 on 2023-05-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0002_truck_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
