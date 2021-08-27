import django_filters
from django_filters import DateFilter
from .models import *


class TransactionFilters(django_filters.FilterSet):
    start_date = DateFilter(field_name='transaction_date', lookup_expr='gte')
    end_date = DateFilter(field_name='transaction_date', lookup_expr='lte')

    class Meta:
        model = CustomerTransaction
        fields = '__all__'
        exclude = ['customer', 'transaction_date']


class CustomerFilters(django_filters.FilterSet):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['date_created']
