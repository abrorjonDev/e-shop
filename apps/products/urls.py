from django.urls import path, include
from rest_framework import routers
from . import views
from . import viewsets

router = routers.DefaultRouter()
router.register(r'products/images', viewsets.ProductImagesViewSet)
router.register(r'products/comments', viewsets.ProductCommentsViewSet)

promo_urlpatterns = [
    path('', views.PromotionListAPIView.as_view(), name='promotion-list-api'),
    path('create/', views.PromotionCreateAPIView.as_view(), name='promotion-create-api'),
    path('<uuid:id>/', views.PromotionRetrieveAPIView.as_view(), name='promotion-retrieve-api'),
    path('<uuid:id>/update/', views.PromotionUpdateAPIView.as_view(), name='promotion-update-api'),
    path('<uuid:id>/delete/', views.PromotionDeleteAPIView.as_view(), name='promotion-delete-api'),
    path('add-remove/<uuid:id>/', views.PromotionAddRemoveAPIView.as_view(), name='promotion-add-remove-api')
]


cat_urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list-api'),
    path('create/', views.CategoryCreateAPIView.as_view(), name='category-create-api'),
    path('<str:slug>/', views.CategoryDetailView.as_view(), name='category-retrieve-api'),
    path('<str:slug>/update/', views.CategoryUpdateAPIView.as_view(), name='category-update-api'),
    path('<str:slug>/delete/', views.CategoryDeleteAPIView.as_view(), name='category-delete-api'),
]

subcat_urlpatterns = [
    path('', views.SubCategoryListView.as_view(), name='subcategory-list-api'),
    path('create/', views.SubCategoryCreateAPIView.as_view(), name='subcategory-create-api'),
    path('<str:slug>/', views.SubCategoryDetailView.as_view(), name='subcategory-retrieve-api'),
    path('<str:slug>/update/', views.SubcategoryUpdateAPIView.as_view(), name='subcategory-update-api'),
    path('<str:slug>/delete/', views.SubcategoryDeleteAPIView.as_view(), name='subcategory-delete-api'),
]

contacts_urlpatterns = [
    path('', views.ContactsListAPIView.as_view(), name='contacts-list-api'),
    path('create/', views.ContactsCreateAPIView.as_view(), name='contacts-create-api'),
    path('<str:slug>/', views.ContactsRetrieveAPIView.as_view(), name='contacts-retrieve-api'),
    path('<str:slug>/update/', views.ContactsUpdateAPIView.as_view(), name='contacts-update-api'),
    path('<str:slug>/delete/', views.ContactsDeleteAPIView.as_view(), name='contacts-delete-api'),
]

urlpatterns = [
    
    path('categories/', include(cat_urlpatterns)),
    
    path('subcategories/', include(subcat_urlpatterns)),
    
    path('products/promotions/', include(promo_urlpatterns)),

    path('contacts/', include(contacts_urlpatterns)),
    
    path('', include(router.urls)),  

    path('products/', views.ProductListCreateView.as_view(), name='products-list-view'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail-view'),
    
] 