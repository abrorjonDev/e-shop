from django.contrib import admin
from tabbed_admin import TabbedModelAdmin
from .models import *

from django.utils.translation import gettext_lazy as _

class ImageInline(admin.TabularInline):
    model = ProductImages
    extra = 0

class SubCategoryInline(admin.TabularInline):
    model = SubCategories
    extra = 0

class ProductInline(admin.TabularInline):
    model = Products
    extra = 0
    exclude = ('title', 'created_at', 'modified_at', 'description')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Title'), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            
        }),
        ( _('IMPORTANTS'), {
            'fields': ('created', 'modified', ('created_at', 'modified_at'))
        })
    )
        
    inlines = (
        SubCategoryInline, ProductInline,
    )

    list_display = ('slug', 'title', 'count_products')
    readonly_fields = ('created_at', 'modified_at')

@admin.register(SubCategories)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'category')
    readonly_fields = ('created_at', 'modified_at')
    list_filter = ('category', )
    fieldsets = (
        (_('Title'), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            
        }),
        ( _('IMPORTANTS'), {
            'fields': ('created', 'modified', ('created_at', 'modified_at'))
        })
    )

    list_per_page = 50


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'price', 'in_promotion')
    # readonly_fields = ('slug', )
    list_filter = ( 'status', 'category', 'sub_category',)
    search_fields = ('category__title', 'sub_category__title', 'title', 'description', 'characteristics')

    prepopulated_fields = {'slug':('title', )}
    list_per_page = 25
    inlines = [ImageInline]
    # fieldsets = {
    #     ''
    # }

@admin.register(ProductImages)
class ProImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'product')
    list_filter = ('product',)
    search_fields = ('product__title', 'image')


@admin.register(Promotions)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_from', 'date_till', 'percentage', 'is_active')
    search_fields = ('title', 'percentage', 'description', 'products__in__title')
    # list_filter = ('is_active',)
    readonly_fields = ('created_at', 'modified_at')
    fieldsets = (
        (_('Title'), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
        }),
        (_('Description'), {
            'fields': ('description_en', 'description_ru', 'description_uz'),  
            'classes':('collapse', )
        }),
        ( _('MAIN PART'), {
            'fields': ('percentage', 'date_from', 'date_till')
        }),
        ( _('IMPORTANTS'), {
            'fields': ('created', 'modified', ('created_at', 'modified_at'))
        }),
        (_('PRODUCTS'), {
            'fields': ('products', ),
            'classes':('collapse', )
        })
    )
    filter_horizontal = ('products',)
    list_per_page = 50