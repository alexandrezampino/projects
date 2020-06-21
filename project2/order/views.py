from django.shortcuts import render, redirect, reverse
from .models import *
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from order.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import transaction
from django.forms import *
from django.http import HttpRequest
from django.db import models
from django_tables2 import SingleTableView
from .tables import *
from .filters import *
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.export.export import TableExport
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


class Headerdetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/Header_detail.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)


        context["Lines"]= Line.objects.filter(po_id=self.kwargs.get('pk'))

        return context

class Headerdetailbooked(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/Order_detail_booked.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)


        context["Lines"]= Line.objects.filter(po_id=self.kwargs.get('pk'))

        return context

class HeaderdetailShipped(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/Order_detail_shipped.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)


        context["Lines"]= Line.objects.filter(po_id=self.kwargs.get('pk'))

        return context


class OrderCreateview(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'order.add_order'
    model= Order
    fields = ['po_number', 'customer', 'shipping_adress', 'comments', 'payment_terms']
    template_name = 'order/lines.html'


    def get_context_data(self, **kwargs):
        #overide the contex datas to make sure formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["Lines"] = LinesFormset(self.request.POST)
        else:
            data["Lines"] = LinesFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        Lines = context["Lines"]

        self.object = form.save()
        if Lines.is_valid():
            Lines.instance = self.object
            Lines.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order:enteredlist')

class Enteredlist(LoginRequiredMixin,ListView):
    model = Order
    fields = ['po_number', 'customer', 'absolute_date', 'total_net_price', 'order_kw']
    template_name = 'order/enteredlist.html'




    ordering = ['-pk']
    #on tilise le queryset de base

    def get_queryset(self):
        queryset = Order.objects.filter(stage='ENTERED')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=OrderFilter(self.request.GET, queryset=self.get_queryset())
        filtering=context['filter']
        context['total_price']=filtering.qs.aggregate(Sum('total_net_price')).get('total_net_price__sum')
        context['total_kw']=filtering.qs.aggregate(Sum('order_kw')).get('order_kw__sum')
        return context

class SupplyCreate(LoginRequiredMixin, CreateView):
    model=Supply_Header
    fields = ['name', 'ETA_date', 'ETD_date']
    template_name = 'order/Newsupply.html'


    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        if self.request.POST:
            data["Lines"] = Supply_Lines_Form(self.request.POST)
        else:
            data["Lines"] = Supply_Lines_Form()
        return data

    def form_valid(self, form):
        data=self.get_context_data()
        Lines=data["Lines"]
        self.object = form.save()
        if Lines.is_valid():


            Lines.instance = self.object
            Lines.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order:Supplylist')





class OrderUpdate(LoginRequiredMixin,UpdateView):
    model= Order
    template_name = 'order/lines.html'
    fields = ['po_number', 'customer', 'shipping_adress', 'comments', 'payment_terms']


    def get_context_data(self, **kwargs):
        #overide the contex datas to make sure formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["Lines"] = LinesFormset(self.request.POST, instance=self.object)
        else:
            data["Lines"] = LinesFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        Lines = context["Lines"]

        self.object = form.save()
        if Lines.is_valid():
            Lines.instance=self.object
            Lines.save()

        return super().form_valid(form)




    def get_form_kwargs(self,**kwargs):
        kwargs=super(OrderUpdate,self).get_form_kwargs(**kwargs)
        return kwargs
        #ne sert a rien car la fonction get_form kwargs n'est pas utilisée

    def get_success_url(self, **kwargs):


        return reverse('order:enteredlist')

class Orderdelete(LoginRequiredMixin,DeleteView):
    model=Order
    success_url = None
    template_name = 'order/Delete_order.html'

    def get_success_url(self):
        return reverse('order:enteredlist')

class BookOrder(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order/book_order.html'
    fields = ['sch_ship_date', 'booked_date']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["Lines"]=Line.objects.filter(po_id=self.kwargs.get('pk'))
        context["product"] = Product.objects.all()
        Lines = context["Lines"]
        prod = context["product"]


        return context

    def form_valid(self, form, **kwargs):
        context=self.get_context_data()
        Lines=context["Lines"]
        prod=context["product"]
        self.object=form.save()
        if form.is_valid():
            form.save
            for object in Lines:
                object.committed_qty=object.quantity
                object.save()



            Order.save(self.object)





        return super().form_valid(form)


    def get_success_url(self):
        return reverse('order:bookedlist')

class BookedView(LoginRequiredMixin,ListView):
        model = Order
        fields = '__all__'
        template_name = 'order/bookedlist.html'

        ordering = ['-pk']
        context_object_name = 'booked'

        def get_queryset(self):
            queryset = {'all_booked': Order.objects.filter(stage='BOOKED')}
            return queryset

class Orderack(LoginRequiredMixin,DetailView):
        model = Order
        template_name = 'order/OrderAck.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            context["Lines"] = Line.objects.filter(po_id=self.kwargs.get('pk'))

            return context


class ShipNotification(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/ShipNotification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["Lines"] = Line.objects.filter(po_id=self.kwargs.get('pk'))

        return context




class Inventoryadj(LoginRequiredMixin,CreateView):
    model = Inventory_ajustments
    template_name = 'order/Inventory_adj.html'
    form_class = Inventoryadjform

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.POST:
            context["adj"]=Inventoryadjform(self.request.POST, instance=self.object)

        return context




    def form_valid(self, form):
        context=self.get_context_data()
        adj= context["adj"]



        if adj.is_valid():
                product=adj.cleaned_data['product']
                prf=Product.objects.all().get(name=product)
                adj.cleaned_data['created_by']=self.request.user
                adj.cleaned_data['created_by'].save()
                adju=Decimal(adj.cleaned_data['quantity'])

                Product.inv_adj(product,adju)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order:inventory')

class Inventorylist(LoginRequiredMixin,ListView) :
        model = Product
        fields = '__all__'
        template_name = 'order/inventory.html'
        context_object_name = 'inventory'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["Product"] = Product.objects.all()
            product = context["Product"]
            for prod in product:
                Product.inv(prod)
                prod.save()
            return context

        def function(self):
            context=self.get_context_data()
            context["Product"] = Product.objects.all()
            product = context["Product"]
            for prod in product:
                Product.inv(prod)
                prod.save()


        def get_queryset(self, **kwargs):
            queryset={'all_product':Product.objects.all()}

            return queryset

class EnteredListView(SingleTableView,ExportMixin, FilterView):
    model=Order
    table_class = enteredList

    template_name = 'order/ListEnteredOrders.html'
    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = OrderFilter(self.request.GET, queryset=self.get_queryset())

        return context


class BookedList(LoginRequiredMixin,ListView):
    model = Order
    fields = ['po_number', 'customer', 'absolute_date', 'total_net_price', 'order_kw']
    template_name = 'order/booklist.html'




    ordering = ['-pk']
    #on tilise le queryset de base

    def get_queryset(self):
        queryset = Order.objects.filter(stage='BOOKED')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=OrderFilter(self.request.GET, queryset=self.get_queryset())
        filtering=context['filter']
        context['total_price']=filtering.qs.aggregate(Sum('total_net_price')).get('total_net_price__sum')
        context['total_kw']=filtering.qs.aggregate(Sum('order_kw')).get('order_kw__sum')
        return context

class Shiporder(LoginRequiredMixin, UpdateView):
        model= Order
        fields= ['shipped_date']
        template_name = 'order/Ship_order.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['order']=Order.objects.filter(pk=self.kwargs.get('pk'))
            return context

        def form_valid(self, form):
            return super().form_valid(form)


        def ship(self,**kwargs):
            context=self.get_context_data()
            order=context['order']

            if order.is_valid():
                order.cleaned_data['shipped_date']=timezone.now()
                order.cleaned_data['shipped_date'].save()
                Order.save(self.object)

class ShippedList(LoginRequiredMixin,ListView):
    model = Order
    fields = ['po_number', 'customer', 'absolute_date', 'total_net_price', 'order_kw']
    template_name = 'order/shippeddlist.html'




    ordering = ['-pk']
    #on tilise le queryset de base

    def get_queryset(self):
        queryset = Order.objects.filter(stage='SHIPPED')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=OrderFilter(self.request.GET, queryset=self.get_queryset())
        filtering=context['filter']
        context['total_price']=filtering.qs.aggregate(Sum('total_net_price')).get('total_net_price__sum')
        context['total_kw']=filtering.qs.aggregate(Sum('order_kw')).get('order_kw__sum')
        return context


class Changeshipdate(LoginRequiredMixin,UpdateView):
    model=Order
    fields=['sch_ship_date']
    template_name = 'order/templates/order/sch_ship_change_order.html'


    def get_success_url(self):
        return reverse('order:bookedlist')

class Invoice(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = InvoiceForm
    template_name = 'order/templates/order/invoice_order.html'
    success_url = None

    def form_valid(self, form):
        return super().form_valid(form)


    def invoice(self):
        context = self.get_context_data()
        order=context['order']
        lines=context['Lines']
        if order.is_valid():
            for order in order:
                pk=order.pk
                terms=order.payment_terms
                order.cleaned_data['invoice_date'].save()
                order.cleaned_data['invoice_number'].save()
                order.fieldsadd=order.fk_payment_terms
                order.fieldsadd.save()
            for lines in lines:
                    prod=lines.product
                    qty=-lines.committed_qty
                    Product.inv_adj(prod,qty)
                    lines.committed_qty=0
                    lines.save()

        return super().form_valid().save()

    def get_context_data(self, *args , **kwargs):
        context=super().get_context_data( *args,**kwargs)
        context['order']= Order.objects.all().filter(pk=self.kwargs.get('pk'))
        context['Lines'] = Line.objects.all().filter(po_id=self.kwargs.get('pk'))
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.all().filter(pk=self.kwargs.get('pk'))
        return queryset

class InvoicedList(LoginRequiredMixin,ListView):
    model = Order
    fields = ['po_number', 'customer', 'absolute_date', 'total_net_price', 'order_kw']
    template_name = 'order/Invoicedlist.html'
    ordering=['-absolute_date']





    #on tilise le queryset de base

    def get_queryset(self):
        queryset = Order.objects.filter(stage='INVOICED')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=OrderFilter(self.request.GET, queryset=self.get_queryset())
        filtering=context['filter']
        context['total_price']=filtering.qs.aggregate(Sum('total_net_price')).get('total_net_price__sum')
        context['total_kw']=filtering.qs.aggregate(Sum('order_kw')).get('order_kw__sum')
        return context

class InvoiceDetail(LoginRequiredMixin, DetailView):
        model = Order
        template_name = 'order/Invoice.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            context["Lines"] = Line.objects.filter(po_id=self.kwargs.get('pk'))

            return context




class Supplylist(LoginRequiredMixin, ListView):
    model=Supply_Header
    fields = ['name', 'ETA_date', 'ETD_date','status']
    template_name = 'order/Supplylist.html'





    ordering = ['-ETA_date']
    #on tilise le queryset de base

    def get_queryset(self):
        queryset = Supply_Header.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SupplyFilter(self.request.GET, queryset=self.get_queryset())
        filtering = context['filter']
        return context





class Supplydetail(LoginRequiredMixin, DetailView):
    model = Supply_Header
    template_name = 'order/supply_detail.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)


        context["Lines"]= Supply_Lines.objects.filter(supply_header_id=self.kwargs.get('pk'))

        return context





