# Generated by Django 5.1.6 on 2025-03-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('megamart', '0002_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
