# Generated by Django 3.2 on 2022-10-28 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0011_merge_20221027_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_picked',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity_available',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
