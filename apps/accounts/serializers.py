from rest_framework import serializers


from .models import CompanyInfo


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"
        read_only_fields = ['created', 'modified']

    def validate(self, attrs):
        if self.instance:
            attrs['modified'] = self.context['request'].user
        else:
            attrs['created'] = self.context['request'].user
        return attrs

    # def create(self, attrs):
    #     attrs['created'] = self.context['request'].user
    #     return super().create(attrs)
    
    # def update(self, instance, attrs):
    #     attrs['modified'] = self.context['request'].user
    #     return super().update(instance, attrs)
