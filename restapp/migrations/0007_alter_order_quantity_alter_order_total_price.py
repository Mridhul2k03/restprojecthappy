# Generated by Django 5.1 on 2024-08-09 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0006_order_permission_doctorspersonalinfo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quandity', to='restapp.productquantity'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total_price', to='restapp.productquantity'),
        ),
    ]
