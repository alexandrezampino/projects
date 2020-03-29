def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["order"] = Order.objects.filter(stage='ENTERED')
    qs = context["order"]
    context["filter"] = OrderFilter(self.request.GET, queryset=self.get_queryset())
    table = context["filter"]
    return context


def get_queryset(self):
    queryset = Order.objects.filter(stage='ENTERED')
    return queryset


def get_table_data(self, **kwargs):
    context = self.get_context_data()
    table = context["filter"]
    self.table = table
    return table
