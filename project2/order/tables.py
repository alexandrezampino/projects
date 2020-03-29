import django_tables2 as tables
from .models import *
from django_tables2 import  TemplateColumn


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)



class enteredList(tables.Table):
    order_number=tables.Column(accessor='po_number', verbose_name='Order number')
    customer = tables.Column(accessor='customer', verbose_name='Customer')
    Date = tables.Column(accessor='absolute_date', verbose_name='Date')
    Net_price= tables.Column(accessor='total_net_price', verbose_name='Net Price',footer=lambda table: sum(x.total_net_price for x in table.data))
    Order_kw = tables.Column(accessor='order_kw', verbose_name='kW',footer=lambda table: sum(x.order_kw for x in table.data))




    class Meta:
        model=Order
        template_name= "django_tables2/bootstrap4.html"
        attrs={'class': 'table table-sm'}
        fields = []

    detail = TemplateColumn(template_name='order/templates/order/pages/tables/Entered_List_Detail.html')

