from django.contrib import admin
from django.urls import path, include
from .views import *
from django_filters.views import FilterView

from django.views.generic.base import TemplateView

app_name = 'order'
urlpatterns = [

    path('order/', OrderCreateview.as_view(), name='new_order'),
    path('order/<pk>', Headerdetail.as_view(), name='order'),
    path('enteredlist/', EnteredListView.as_view(filterset_class=OrderFilter), name='entered'),
    path('update/<pk>', OrderUpdate.as_view(), name='updateorder'),
    path('delete/<pk>', Orderdelete.as_view(), name='deleteorder'),
    path('order/<pk>/book', BookOrder.as_view(), name='book'),
    path('bookedlist/', BookedList.as_view(), name='bookedlist'),
    path('orderack/<pk>', Orderack.as_view(), name='orderack'),
    path('booked/<pk>', Headerdetailbooked.as_view(), name='booked'),
    path('inventory/', Inventorylist.as_view(), name='inventory'),
    path('inventoryadj/', Inventoryadj.as_view(), name='inventoryadj'),
    path('entered/', Enteredlist.as_view(), name='enteredlist'),
    path('ship/<pk>',Shiporder.as_view(),name='ship'),
    path('shippedlist', ShippedList.as_view(), name='shippedlist'),
    path('changeshipdate/<pk>', Changeshipdate.as_view(), name='changeshipdate'),
    path('invoice/<pk>', Invoice.as_view(), name='invoice'),
    path('shipped/<pk>', Invoice.as_view(), name='invoice')

]