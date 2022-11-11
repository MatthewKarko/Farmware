# Generated by Django 3.2.16 on 2022-11-10 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_api', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
            },
        ),
        migrations.CreateModel(
            name='OrderItemStockLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
            ],
            options={
                'verbose_name': 'order item stock link',
                'verbose_name_plural': 'order item stock links',
            },
        ),
        migrations.RemoveField(
            model_name='orderstock',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='orderstock',
            name='quantity_suffix_id',
        ),
        migrations.RemoveField(
            model_name='orderstock',
            name='stock_id',
        ),
        migrations.AlterModelOptions(
            name='areacode',
            options={'verbose_name': 'area code', 'verbose_name_plural': 'area codes'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'customer', 'verbose_name_plural': 'customers'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'order', 'verbose_name_plural': 'orders'},
        ),
        migrations.AlterModelOptions(
            name='organisation',
            options={'verbose_name': 'organisation', 'verbose_name_plural': 'organisations'},
        ),
        migrations.AlterModelOptions(
            name='produce',
            options={'verbose_name': 'produce', 'verbose_name_plural': 'produce'},
        ),
        migrations.AlterModelOptions(
            name='producequantitysuffix',
            options={'verbose_name': 'produce quantity suffix', 'verbose_name_plural': 'produce quantity suffixes'},
        ),
        migrations.AlterModelOptions(
            name='producevariety',
            options={'verbose_name': 'produce variety', 'verbose_name_plural': 'produce varieties'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-date_picked'], 'verbose_name': 'stock', 'verbose_name_plural': 'stock'},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'verbose_name': 'supplier', 'verbose_name_plural': 'suppliers'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'team', 'verbose_name_plural': 'teams'},
        ),
        migrations.AddField(
            model_name='order',
            name='completion_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='quantity_available',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='invoice_number',
            field=models.TextField(blank=True, max_length=20, null=True),
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
            name='date_completed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_picked',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_planted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_seeded',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ehd',
            field=models.DateField(blank=True, null=True),
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
        migrations.AddConstraint(
            model_name='produce',
            constraint=models.UniqueConstraint(fields=('name', 'organisation'), name='unique_name_organisation_combination'),
        ),
        migrations.DeleteModel(
            name='OrderStock',
        ),
        migrations.AddField(
            model_name='orderitemstocklink',
            name='order_item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.orderitem'),
        ),
        migrations.AddField(
            model_name='orderitemstocklink',
            name='quantity_suffix_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producequantitysuffix'),
        ),
        migrations.AddField(
            model_name='orderitemstocklink',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.stock'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='produce_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.produce'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='produce_variety_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producevariety'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity_suffix_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.producequantitysuffix'),
        ),
    ]
