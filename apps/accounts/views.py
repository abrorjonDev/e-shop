from django.shortcuts import render

# TO DO
    # LOGIN
    # LOGOUT
    # PASSWORD RESET
    # PASSWORD CHANGE
    # REGISTER
from .models import CompanyInfo
from rest_framework.viewsets import ModelViewSet
class CompanyDataAPIView(ModelViewSet):
    queryset = CompanyInfo
    serializer_class = CompanyInfoSerializer
    
