# Generated by Django 3.2.16 on 2022-10-21 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0007_auto_20221022_0809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-date_picked'], 'verbose_name': 'stock', 'verbose_name_plural': 'stock'},
        ),
    ]