# Generated by Django 3.2.6 on 2021-08-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'DRAFT'), (2, 'NEW'), (3, 'ACCEPT'), (4, 'PICKUP')], default=1),
        ),
    ]
