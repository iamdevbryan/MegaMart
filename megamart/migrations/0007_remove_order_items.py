# Generated by Django 5.1.6 on 2025-03-15 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('megamart', '0006_order_items_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]
