# Generated by Django 3.2.16 on 2022-10-29 05:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_api', '0012_auto_20221028_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.customer'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='produce_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.produce'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='produce_variety_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producevariety'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity_suffix_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producequantitysuffix'),
        ),
        migrations.AlterField(
            model_name='orderitemstocklink',
            name='quantity_suffix_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producequantitysuffix'),
        ),
        migrations.AlterField(
            model_name='producequantitysuffix',
            name='produce_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.produce'),
        ),
        migrations.AlterField(
            model_name='producevariety',
            name='produce_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.produce'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='area_code_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.areacode'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='produce_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.produce'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity_suffix_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producequantitysuffix'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.supplier'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='variety_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producevariety'),
        ),
        migrations.AlterField(
            model_name='stockpickers',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
