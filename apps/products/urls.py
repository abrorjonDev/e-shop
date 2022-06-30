from django.urls import path, include

from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list-create-view'),
    path('categories/<str:slug>/', views.CategoryDetailView.as_view(), name='category-retrieve-update-delete-view'),

    path('subcategories/', views.SubCategoryListView.as_view(), name='subcategory-list-create-view'),
    path('subcategories/<str:slug>/', views.SubCategoryDetailView.as_view(), name='subcategory-retrieve-update-delete-view'),
]