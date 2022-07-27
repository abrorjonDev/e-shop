from django_filters import rest_framework as filter
import django_filters

from . import models
from django.utils import timesince, timezone
 

class CategoryFilterSet(filter.FilterSet):
    class Meta:
        model = models.Categories
        fields = ['title'] 

class ProductFilterSet(filter.FilterSet):

    def get_categories(self):
        return models.Categories.objects.all()


    def get_subcategories(self):
        return models.SubCategories.objects.all()


    category = django_filters.ModelChoiceFilter(queryset=get_categories, lookup_expr='exact')
    sub_category = django_filters.ModelChoiceFilter(queryset=get_subcategories, lookup_expr='exact')
    top = django_filters.BooleanFilter(field_name='seen', method='get_top_products')
    new = django_filters.BooleanFilter(label='New products', method='get_new_products')
    class Meta:
        model = models.Products
        fields = ['title', 'category', 'sub_category', 'description', 'characteristics', 'status', 'price', ]


    def get_top_products(self, queryset, name, value):
        if value is True:
            return queryset.filter(status=models.Products.STATUS.in_stock).order_by('-seen',)[:20]
        return queryset

    def get_new_products(self, queryset, name, value):
        if value is True:
            return queryset.order_by('-modified_at', '-created_at', )
        return queryset


class ContactsFilter(filter.FilterSet):
    class Meta:
        model = models.Contacts
        fields = {
            'name': ['icontains', ],
            'status': ['exact']
        }