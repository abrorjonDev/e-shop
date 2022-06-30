from django.contrib import admin

from .models import *



class ImageInline(admin.TabularInline):
    model = ProductImages
    extra = 0



admin.site.register(Categories)

admin.site.register(SubCategories)

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'price', 'in_promotion')
    # readonly_fields = ('slug', )

    prepopulated_fields = {'slug':('title', )}
    list_per_page = 25
    inlines = [ImageInline]
    # fieldsets = {
    #     ''
    # }

admin.site.register(ProductImages)


admin.site.register(Promotions)





