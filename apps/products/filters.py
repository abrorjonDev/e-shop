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
    price_greater = django_filters.NumberFilter(label='Price greater than you entered', 
                                                method='get_price_UZS_greater_than')
    price_less = django_filters.NumberFilter(label='Price is less than you entered', 
                                                method='get_price_less_then')
    
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

    def get_price_UZS_greater_than(self, queryset, name, value):
        active_currency = models.Currency.objects.last()
        value = value / active_currency.value if (active_currency is not None and active_currency.value != 0) else value
        return queryset.filter(price__gte=value)

    def get_price_less_then(self, queryset, name, value):
        active_currency = models.Currency.objects.last()
        value = value / active_currency.value if (active_currency is not None and active_currency.value != 0) else value
        return queryset.filter(price__lte=value)

class ContactsFilter(filter.FilterSet):
    class Meta:
        model = models.Contacts
        fields = {
            'name': ['icontains', ],
            'status': ['exact']
        }