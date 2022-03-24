# Generated by Django 3.2.6 on 2021-11-18 06:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0007_alter_product_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateTrigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.IntegerField(choices=[(1, 'Show Order To Offer'), (2, 'Notify Driver Exp Accept'), (3, 'Return To Offer')])),
                ('time_run', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'CreateTrigger',
                'verbose_name_plural': 'CreateTriggers',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RunTrigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('finished_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Progress'), (3, 'Done'), (4, 'Failed')], default=1)),
                ('error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'RunTrigger',
                'verbose_name_plural': 'RunTriggers',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'New'), (4, 'Accept'), (8, 'Pickup')], default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'New'), (4, 'Accept'), (8, 'Pickup')], default=1),
        ),
    ]