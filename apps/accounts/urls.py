from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompanyDataAPIView

router = DefaultRouter()

router.register(r'company', CompanyDataAPIView, basename='company-data')


urlpatterns = []+router.urls

