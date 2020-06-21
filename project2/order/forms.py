from django import forms
from .models import *
from django.forms.models import inlineformset_factory, formset_factory
from django.forms import ModelForm


class Header_form(forms.Form):
    class Meta:
        model = Order
        fields = '__all__'


class Headerdetail_form(forms.Form):
    class Meta:
        model = Order


class bookorder(forms.Form):
    class Meta:
        model = Order
        fields = ['sch_ship_date']


class Inventoryadjform(ModelForm):
    class Meta:
        model = Inventory_ajustments
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['invoice_date', 'invoice_number']


class LinesCreationForm(forms.Form):
    class Meta:
        model = Line
        exclude = ()


class Lineform(forms.Form):
    class Meta:
        model = Line
        fields = ['product', 'quantity', 'unit_price', 'line_vat']


LinesFormset = inlineformset_factory(Order, Line, fields=('product', 'quantity', 'unit_price', 'line_vat'), extra=4)
LineFormset = formset_factory(Line, extra=2, can_delete=True)

Supply_Lines_Form = inlineformset_factory(Supply_Header, Supply_Lines, fields=(
    'supply_product', 'supply_quantity', 'supply_unit_price'), extra=4, can_delete=True)
