import django_filters
from . import models

class MenuItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='iexact')
    to_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    from_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = models.MenuItem
        fields = ['title', 'category', 'to_price', 'from_price']

class OrderFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='orderitem__menuitem__title', lookup_expr='icontains')
    delivery_crew = django_filters.CharFilter(field_name='delivery_crew__username', lookup_expr='icontains')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    category = django_filters.CharFilter(field_name='orderitem__menuitem__category__title', lookup_expr='iexact')
    to_total = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    from_total = django_filters.NumberFilter(field_name='total', lookup_expr='gte')

    class Meta:
        model = models.Order
        fields = ['title', 'delivery_crew', 'start_date', 'category', 'to_total', 'from_total']
