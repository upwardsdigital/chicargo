# Generated by Django 4.2.1 on 2023-07-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_product_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
