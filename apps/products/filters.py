from django_filters import rest_framework as filter
import django_filters

from . import models

 

class CategoryFilterSet(filter.FilterSet):
    class Meta:
        model = models.Categories
        fields = ['title'] 

class ProductFilterSet(filter.FilterSet):

    def get_categories(self):
        return models.Categories.objects.all()


    def get_subcategories(self):
        return models.SubCategories.objects.all()


    category = django_filters.ModelChoiceFilter(queryset=get_categories)
    sub_category = django_filters.ModelChoiceFilter(queryset=get_subcategories)

    class Meta:
        model = models.Products
        fields = ['title', 'category', 'sub_category', 'description', 'characteristics', 'status', 'price', ]


    