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




class LinesCreationForm(forms.Form):
    class Meta:
        model = Line
        exclude=()

class Lineform(forms.Form):
    class Meta:
        model = Line
        fields = ['product', 'quantity','unit_price', 'line_vat']

LinesFormset=inlineformset_factory(Order, Line, fields=('product', 'quantity','unit_price', 'line_vat'), extra=4)
LineFormset = formset_factory(Line, extra=2, can_delete=True)