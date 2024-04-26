# Generated by Django 5.0.4 on 2024-04-26 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_rename_location_restaurant_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.TextField(default='No description available'),
        ),
    ]
