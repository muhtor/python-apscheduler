# Generated by Django 3.2.6 on 2021-08-18 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0006_product_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]
