# Generated by Django 3.2.6 on 2021-08-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_alter_order_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('status', models.IntegerField(choices=[(1, 'DRAFT'), (2, 'NEW'), (3, 'ACCEPT'), (4, 'PICKUP')], default=1)),
            ],
        ),
    ]
