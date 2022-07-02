from django.urls import path, include
from rest_framework import routers
from . import views, viewsets

router = routers.DefaultRouter()
router.register(r'products/images', viewsets.ProductImagesViewSet)
router.register(r'products/comments', viewsets.ProductCommentsViewSet)
router.register(r'products/promotions', viewsets.PromotionViewSet)
router.register(r'products/promotions/add-remove', viewsets.PromotionProductAddRemoveViewSet)


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list-create-view'),
    path('categories/<str:slug>/', views.CategoryDetailView.as_view(), name='category-retrieve-update-delete-view'),

    path('subcategories/', views.SubCategoryListView.as_view(), name='subcategory-list-create-view'),
    path('subcategories/<str:slug>/', views.SubCategoryDetailView.as_view(), name='subcategory-retrieve-update-delete-view'),

    path('', include(router.urls)),  

    path('products/', views.ProductListCreateView.as_view(), name='products-list-view'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail-view'),
    
] 