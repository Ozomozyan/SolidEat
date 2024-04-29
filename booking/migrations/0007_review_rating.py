# Generated by Django 5.0.4 on 2024-04-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_restaurant_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
    ]
