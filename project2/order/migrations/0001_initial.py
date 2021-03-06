# Generated by Django 3.0.2 on 2020-05-18 11:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse_shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('line1', models.CharField(blank=True, max_length=300, null=True)),
                ('line2', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=8, null=True)),
                ('iso_code', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('vat_number', models.CharField(blank=True, max_length=20, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bill_line1', models.CharField(blank=True, max_length=300, null=True)),
                ('bill_line2', models.CharField(blank=True, max_length=300, null=True)),
                ('bill_city', models.CharField(blank=True, max_length=50, null=True)),
                ('bill_zipcode', models.CharField(blank=True, max_length=8, null=True)),
                ('bill_iso_code', models.CharField(blank=True, max_length=2, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('sales_rep', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_rep', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_terms_choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('wattage', models.DecimalField(decimal_places=0, default=0, max_digits=6)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=6)),
                ('inventory_committed', models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=6)),
                ('inventory_entered', models.DecimalField(decimal_places=0, default=0, editable=False, max_digits=6)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supply_Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Supply', max_length=500)),
                ('ETA_date', models.DateField(blank=True, null=True)),
                ('ETD_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(default='In transit', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Supply_Lines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supply_quantity', models.DecimalField(decimal_places=0, max_digits=6)),
                ('supply_unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('supply_header', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supply_header', to='order.Supply_Header')),
                ('supply_product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supply_product', to='order.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.Product_type'),
        ),
        migrations.CreateModel(
            name='Payment_terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('delta', models.DecimalField(decimal_places=0, default=0, max_digits=2)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='type', to='order.Payment_terms_choices')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('booked_date', models.DateField(blank=True, null=True)),
                ('sch_ship_date', models.DateField(blank=True, null=True)),
                ('shipped_date', models.DateField(blank=True, null=True)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('stage', models.CharField(default='ENTERED', max_length=100)),
                ('total_net_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('total_order_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('absolute_date', models.DateField(blank=True, null=True)),
                ('order_kw', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('invoice_due_date', models.DateField(blank=True, null=True)),
                ('str_payterms', models.CharField(blank=True, default='bla', max_length=50, null=True)),
                ('str_pay_type', models.CharField(blank=True, default='bla', max_length=50, null=True)),
                ('str_pay_days', models.CharField(blank=True, default='bla', max_length=50, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.Customer')),
                ('payment_terms', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_terms', to='order.Payment_terms')),
                ('shipping_adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.Adresse_shipping')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('line_vat', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)])),
                ('net_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('kw', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('committed_qty', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('po', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='po', related_query_name='po_query', to='order.Order', verbose_name='po')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product', related_query_name='product_query', to='order.Product')),
            ],
            options={
                'verbose_name': 'Line',
                'verbose_name_plural': 'Lines',
            },
        ),
        migrations.CreateModel(
            name='Inventory_ajustments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('reason', models.CharField(max_length=200)),
                ('quantity', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.Product')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_quantity', models.DecimalField(decimal_places=0, max_digits=6)),
                ('forecast_month_start', models.DateField()),
                ('forecast_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('forecast_product', models.ForeignKey(limit_choices_to={'Type': 'Micro'}, on_delete=django.db.models.deletion.PROTECT, related_name='forecast_product', to='order.Product')),
                ('forecast_sales_rep', models.ForeignKey(limit_choices_to={'is_staff': False}, on_delete=django.db.models.deletion.CASCADE, related_name='forecast_sales_rep', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='adresse_shipping',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.Customer'),
        ),
    ]
