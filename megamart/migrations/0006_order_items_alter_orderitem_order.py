# Generated by Django 5.1.6 on 2025-03-14 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('megamart', '0005_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order_items', to='megamart.orderitem'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items_set', to='megamart.order'),
        ),
    ]
