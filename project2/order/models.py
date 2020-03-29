from django.conf import settings, global_settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import *
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import *
from django.utils import timezone
from django.urls import reverse
from django.utils.dateparse import parse_date
CURRENCY=settings.CURRENCY
# Create your models here.

class Payment_terms_choices(models.Model):
    name=models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Payment_terms(models.Model):
    name=models.CharField(max_length=20)
    type = models.ForeignKey(Payment_terms_choices, on_delete=models.PROTECT,blank=True,null=True )
    delta=models.DecimalField(max_digits=2, decimal_places=0, default=0)

    def __str__(self):
        return ('%s %s' % (self.delta,self.type))

class Customer(models.Model):

    name=models.CharField(max_length=100, blank=True, null=True)
    sales_rep = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_rep')
    vat_number=models.CharField(max_length=20, blank=True, null=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null= True)
    created_date=models.DateTimeField(default=timezone.now)
    bill_line1 = models.CharField(max_length=300, blank=True, null=True)
    bill_line2 = models.CharField(max_length=300, blank=True, null=True)
    bill_city = models.CharField(max_length=50, blank=True, null=True)
    bill_zipcode = models.CharField(max_length=8, blank=True, null=True)
    bill_iso_code = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Adresse_shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, blank=True, null=True)
    line1=models.CharField(max_length=300, blank=True, null=True)
    line2  = models.CharField(max_length=300, blank=True, null=True)
    city=models.CharField(max_length=50, blank=True, null=True)
    zipcode=models.CharField(max_length=8, blank=True, null=True )
    iso_code=models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return ('%s %s' % (self.customer, self.name))

class Product_type(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=50, blank=True, null=True, name='name', unique=True)
    code=models.CharField(max_length=50, blank=True, null=True)
    type=models.ForeignKey(Product_type, on_delete=models.PROTECT)
    wattage=models.DecimalField(name='wattage', max_digits=6, decimal_places=0, default=0)
    active=models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null= True)
    inventory = models.DecimalField(name='inventory', decimal_places=0, max_digits=6, default=0, editable=False)
    inventory_committed = models.DecimalField(name='inventory_committed', decimal_places=0, max_digits=6, default=0, editable=False)
    inventory_entered = models.DecimalField(name='inventory_entered', decimal_places=0, max_digits=6, default=0, editable=False)

    def inv_adj(self, quantity):
        self.inventory += quantity
        super(Product, self).save()

    def inv(self, *args, **kwargs):


        Line_items = Line.objects.filter(product__name=self, po__stage='ENTERED')
        self.inventory_entered=Decimal(Line_items.aggregate(Sum('quantity'))['quantity__sum'] if Line_items.exists() else 100.00)

        Line_items_committed=Line.objects.filter(product__name=self)
        self.inventory_committed=Decimal(Line_items_committed.aggregate(Sum('committed_qty'))['committed_qty__sum'] if Line_items_committed.exists() else 0.00)

        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    def _get_wattage(self):
        watt=self.wattage
        return watt

class Inventory_ajustments(models.Model):
    class Meta:
        ordering=['-created_date']

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True)
    created_date = models.DateField(default=timezone.now, name='created_date')
    reason=models.CharField(max_length=200, name='reason')
    product=models.ForeignKey(Product, name='product', on_delete=models.PROTECT)
    quantity=models.DecimalField(name='quantity', max_digits=6, decimal_places=0, default=0, blank=True, null=True)


class Order(models.Model):
    STAGE_CHOICES = ( ("ENTERED"),("BOOKED"), ("SHIPPED"), ("INVOICED") )

    class Meta:
        verbose_name= "Order"
        verbose_name_plural="Orders"


    po_number=models.CharField(max_length=50, blank=True, null=True, name='po_number')
    created_date = models.DateField(default=timezone.now, name='created_date')
    customer=models.ForeignKey(Customer, blank=True, null=True,on_delete=models.PROTECT, name='customer')
    shipping_adress=models.ForeignKey(Adresse_shipping, blank=True, null=True, on_delete=models.PROTECT, name='shipping_adress')
    comments=models.CharField(blank=True, null=True, max_length=200, name='comments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null= True)
    booked_date=models.DateField(blank=True, null=True, name='booked_date')
    sch_ship_date=models.DateField(blank=True, null=True, name='sch_ship_date')
    shipped_date=models.DateField(blank=True, null=True, name='shipped_date')
    invoice_date=models.DateField(blank=True, null=True)
    stage=models.CharField(max_length=100, default='ENTERED')
    total_net_price=models.DecimalField(name='total_net_price', blank=True, null=True, max_digits=10, decimal_places=2,
                                        default=0)
    total_order_price = models.DecimalField(name='total_order_price', blank=True, null=True, max_digits=10,
                                          decimal_places=2, default=0)
    absolute_date=models.DateField(blank=True, null=True)
    order_kw=models.DecimalField(name='order_kw', blank=True, null=True, max_digits=10, decimal_places=2, default=0)
    invoice_number=models.CharField(max_length=50,default='Inv-01', name='invoice_number')
    invoice_balance=models.DecimalField(name='invoice_balance', blank=True, null=True,default=0, decimal_places=2,
                                        max_digits=10)
    payment_date=models.DateField(name='payment_date', blank=True, null=True)
    payment_terms=models.ForeignKey(Payment_terms, on_delete=models.PROTECT,blank=True, null=True, default=1, name='payment_terms')


    def tag_total_order_price(self):
        return f'{self.total_order_price} {CURRENCY}'

    def get_stage(self):
        stage=self.stage
        return stage

    def ship(self, args, **kwargs):
        self.shipped_date=timezone.now()
        self.shipped_date.save()
        super().save(self,*args, **kwargs)

    def post_save(self, *args, **kwargs):
            if self.invoice_date is not None:
                self.absolute_date=self.invoice_date
                self.stage='INVOICED'
            elif self.invoice_date is None and self.shipped_date is not None:
                self.absolute_date=self.shipped_date
                self.stage='SHIPPED'
            elif self.invoice_date is None and self.shipped_date is None and self.sch_ship_date is not None:
                self.absolute_date=self.sch_ship_date
                self.stage='BOOKED'
                self.booked_date=timezone.now()
            elif self.booked_date is None:
                self.absolute_date=self.created_date

            super().save(*args, **kwargs)



    def save(self, *args, **kwargs):
        order_items=self.po.all()
        self.total_net_price=order_items.aggregate(Sum('net_price'))['net_price__sum'] if order_items.exists() else 0.00
        self.total_net_price=Decimal(self.total_net_price)
        self.total_order_price=order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        self.total_order_price=Decimal(self.total_order_price)
        self.order_kw=order_items.aggregate(Sum('kw'))['kw__sum'] if order_items.exists() else 0.00
        self.order_kw=Decimal(self.order_kw)
        if self.invoice_date is not None:
            self.absolute_date = self.invoice_date
            self.stage = 'INVOICED'
        elif self.invoice_date is None and self.shipped_date is not None:
            self.absolute_date = self.shipped_date
            self.stage = 'SHIPPED'
        elif self.invoice_date is None and self.shipped_date is None and self.sch_ship_date is not None:
            self.absolute_date = self.sch_ship_date
            self.stage = 'BOOKED'
            self.booked_date = timezone.now()
        elif self.booked_date is None:
            self.absolute_date = self.created_date

        super().save(*args, **kwargs)




    def get_absolute_url(self, **kwargs):
        return reverse('order:order', kwargs={'pk': self.pk})



    def __str__(self):
        return self.pk


class Line(models.Model):
    class Meta:
        verbose_name="Line"
        verbose_name_plural="Lines"

    po=models.ForeignKey(Order,verbose_name='po',blank=True, null=True,on_delete=models.CASCADE, related_name='po', related_query_name='po_query')
    product=models.ForeignKey(Product,blank=True, null=True,on_delete=models.PROTECT, related_name='product', related_query_name='product_query')
    quantity=models.DecimalField(name='quantity', max_digits=10, decimal_places=0, default=0)
    unit_price=models.DecimalField(name='unit_price', max_digits=10, decimal_places=2, default=0)
    line_vat=models.DecimalField(name='line_vat', max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
    net_price=models.DecimalField(name='net_price', max_digits=10, decimal_places=2, default=0)
    total_price=models.DecimalField(name='total_price', max_digits=10, decimal_places=2, default=0)
    kw=models.DecimalField(name='kw', max_digits=10, decimal_places=2, default=0)
    committed_qty=models.DecimalField(name='committed_qty', max_digits=10, decimal_places=2, default=0, null=True,blank=True)

    @property
    def stage(self):
        stage = Order.get_stage(self.po)
        return stage



    def get_absolute_url(self):
        return reverse('order:order', pk=self.pk)

    def save(self, *args, **kwargs):
        self.net_price=Decimal(self.quantity)*Decimal(self.unit_price)
        self.total_price=(Decimal(self.line_vat)/100+Decimal(1))*Decimal(self.net_price)
        if self.product is not None:
            watt= Product._get_wattage(self.product)
            watt=Decimal(watt)*Decimal(self.quantity)
            self.kw=watt/1000

        super().save(*args, **kwargs)

    def book_commit(self,*args, **kwargs):
        stage = Order.get_stage(self.po)
        if self.product is not None:
            if stage is not 'ENTERED' and stage is not 'INVOICED':
                self.committed_qty=self.quantity

        super().save(*args,**kwargs)











