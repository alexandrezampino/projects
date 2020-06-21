import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
    date2 = django_filters.DateFilter(field_name='absolute_date', lookup_expr='gte', label= 'Date low range')
    date= django_filters.DateFilter(field_name='absolute_date', lookup_expr='lte', label='Date high range')



    class Meta:
        model = Order
        fields = ['customer', 'customer__sales_rep']


class SupplyFilter(django_filters.FilterSet):

    ETA_date = django_filters.DateFilter(field_name='ETA_date', lookup_expr='gte', label= 'Date low range')
    ETA_date2= django_filters.DateFilter(field_name='ETA_date', lookup_expr='lte', label='Date high range')
    status=django_filters.CharFilter(field_name='status', lookup_expr='icontains')


    class Meta:
        model = Supply_Header
        fields = ['ETA_date']


