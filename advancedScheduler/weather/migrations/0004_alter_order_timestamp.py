# Generated by Django 3.2.6 on 2021-08-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
