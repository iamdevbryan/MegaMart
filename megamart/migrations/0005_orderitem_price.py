# Generated by Django 5.1.6 on 2025-03-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('megamart', '0004_order_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
