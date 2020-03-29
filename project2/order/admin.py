from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Customer)
admin.site.register(Adresse_shipping)
admin.site.register(Product_type)
admin.site.register(Product)
admin.site.register(Payment_terms)
admin.site.register(Payment_terms_choices)
class Product(admin.ModelAdmin):
    exclude=('inventory')
