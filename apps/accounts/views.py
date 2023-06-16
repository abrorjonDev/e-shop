from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import CompanyInfoSerializer
from .models import CompanyInfo


class CompanyDataAPIView(ModelViewSet):
    """
    All methods are built-in methods in ViewSet.
    It's unefficient, but more faster in dev process.
    """
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
