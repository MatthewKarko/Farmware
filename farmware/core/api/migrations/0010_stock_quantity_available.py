# Generated by Django 3.2.16 on 2022-10-27 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0009_auto_20221026_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='quantity_available',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
