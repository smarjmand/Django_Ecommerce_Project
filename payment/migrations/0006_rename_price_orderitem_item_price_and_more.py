# Generated by Django 5.1.2 on 2024-11-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_order_track_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='item_price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_cost',
            field=models.IntegerField(default=0),
        ),
    ]
