from rest_framework import serializers


from .models import CompanyInfo


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"
        read_only_fields = ['created', 'modified']

        
