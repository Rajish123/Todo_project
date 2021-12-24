import django_filters
from django_filters import DateFilter,CharFilter
from .models import *

class SearchFilter(django_filters.FilterSet):
    description = CharFilter(field_name = 'description', lookup_expr = 'icontains')
    date = DateFilter(field_name = 'created_at', lookup_expr = 'lte')
    class Meta:
        model = Todo
        fields = ['title']