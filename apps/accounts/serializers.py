from rest_framework import serializers


from .models import CompanyInfo


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"
        read_only_fields = ['created', 'modified']

    def create(self, attrs):
        company = super().create(attrs)
        company.created = self.context['request'].user
        company.save()
        return company
    
    def update(self, instance, attrs):
        instance = super().update(instance, attrs)
        instance.modified = self.context['request'].user
        instance.save()
        return instance
