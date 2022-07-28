from rest_framework import serializers

from rest_framework.generics import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import *

from .validators import validate_slug

class PromotionListSerializer(serializers.ModelSerializer):
    # is_active = serializers.BooleanField(read_only=True)
    # created = serializers.CharField(source='created.username', required=False)
    # modified =  serializers.CharField(source='modified.username', required=False)
    class Meta:
        model = Promotions
        fields = ("id", "title", "percentage", "is_active", ) #  "created", "modified")

    extra_kwargs = {
        "date_from":{"write_only":True, },
        "date_till":{"write_only":True, }

    }

class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("id", 'image') # "imageURL",

class ProductsListSerializer(serializers.ModelSerializer):
    
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(read_only=True, many=False)
    thumbnail = ProductImagesListSerializer(read_only=True, many=False)

    class Meta:
        model = Products
        fields = ("slug", "title", "status", "price", "comments_count", "in_promotion", "thumbnail", "seen")

    

class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ("slug", "title", 'imageURL')


class SubcategorySerializer(serializers.ModelSerializer):
    # products = ProductsListSerializer(required=False, many=True)
    products = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.title", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    class Meta:
        model = SubCategories
        fields = ("slug", "title", "title_en", "title_ru", "title_uz", "category", "products", "category_name", "category_slug", "image", "imageURL")
        read_only_fields = ('title', "imageURL")
        extra_kwargs = {
            'title_en': {'write_only':True},
            'title_ru': {'write_only':True},
            'title_uz': {'write_only':True},
            'category': {'write_only':True},
            'image': {'write_only':True},
        }
    
    def get_products(self, obj):
        response = ProductsListSerializer(obj.products.all(), many=True).data
        return response


class CategoryListCreateSerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(read_only=True, many=True)
    slug = serializers.SlugField(read_only=True)
    imageURL = serializers.CharField(read_only=True)
    title_en = serializers.CharField(validators=[validate_slug], write_only=True)
    title_ru = serializers.CharField(validators=[validate_slug], write_only=True)
    title_uz = serializers.CharField(validators=[validate_slug], write_only=True)

    class Meta:
        model = Categories
        fields = ("slug", "title", "title_en","title_ru", "title_uz", "subcategories", "image", "imageURL")
        read_only_fields = ('title', 'subcategories', "imageURL")
        extra_kwargs = {
            'image': {'write_only':True},
        }

    def create(self, attrs):
        category = Categories(
            **attrs,
            created=self.context['request'].user
        )
        category.save()
        return category

    def update(self, instance, attrs):
        instance.modified = self.context['request'].user
        instance.modified_at = timezone.now()
        return super().update(instance, attrs)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(read_only=True, many=True)
    products = ProductsListSerializer(read_only=True, many=True)
    imageURL = serializers.CharField(read_only=True)
    title_en = serializers.CharField(validators=[validate_slug], write_only=True)
    title_ru = serializers.CharField(validators=[validate_slug], write_only=True)
    title_uz = serializers.CharField(validators=[validate_slug], write_only=True)
    class Meta:
        model = Categories
        fields = ("slug", "title","title_en","title_ru", "title_uz","subcategories", "products", "image", "imageURL")
        read_only_fields = ['slug', "subcategories", "products", 'title', "imageURL"]

        extra_kwargs = {
            'image': {'write_only':True},
        }

    def update(self, instance, attrs):
        instance.modified = self.context['request'].user
        return super().update(instance, attrs)


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComments
        fields = ("id", "name", "review", "comment", )

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentsListSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(many=False, read_only=True)
    images = ProductImagesListSerializer(required=False, many=True)
    category_name = serializers.CharField(source="category.title",read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    subcategory_name = serializers.CharField(source="sub_category.title",read_only=True)
    subcategory_slug = serializers.CharField(source="sub_category.slug", read_only=True)

    similar_products = ProductsListSerializer(many=True, read_only=True)
    
    title_en = serializers.CharField(validators=[validate_slug], write_only=True)
    title_ru = serializers.CharField(validators=[validate_slug], write_only=True)
    title_uz = serializers.CharField(validators=[validate_slug], write_only=True)

    class Meta:
        model = Products
        fields = (
            "slug", "title", "title_en","title_ru", "title_uz",
            "category", "category_name", "category_slug",
            "sub_category", "subcategory_name", "subcategory_slug",
            "description_en", "description_ru","description_uz", "characteristics_en", "characteristics_ru", "characteristics_uz", 'status', 'price', 'quantity',
            'comments', 'comments_count', 'in_promotion','similar_products',
            'images', 'seen',
        )
        read_only_fields = [
             'title', "description", "characteristics",'seen', 'slug',
            ]
        extra_kwargs = {
            'title_en': {'write_only':True},
            'title_ru': {'write_only':True},
            'title_uz': {'write_only':True},
            'description_en': {'write_only':True},
            'description_ru': {'write_only':True},
            'description_uz': {'write_only':True},
            'characteristics_ru': {'write_only':True},
            'characteristics_uz': {'write_only':True},
            'characteristics_en': {'write_only':True}
        }

    def create(self, attrs):
        product = super().create(attrs)
        product.created = self.context['request'].user
        product.save()
        
        return product

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if data.get('title_en', None):
    #         del data['title_en']
    #     return data

class ProductUpdateSerializer(serializers.ModelSerializer):
    title_en = serializers.CharField(validators=[validate_slug], write_only=True)
    title_ru = serializers.CharField(validators=[validate_slug], write_only=True)
    title_uz = serializers.CharField(validators=[validate_slug], write_only=True)

    class Meta:
        model = Products
        exclude = ('title', 'description', 'characteristics', )
        read_only_fields = ['created_by', 'modified_by']


    def update(self, instance, attrs):
        instance.modified = self.context['request'].user
        
        return super().update(instance, attrs)

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"
        read_only_fields = ('created', 'modified')

    def create(self, attrs):
        attrs['created'] = self.context['request'].user
        return super().create(attrs)

    def update(self, instance, attrs):
        attrs['modified'] = self.context['request'].user
        return super().update(instance, attrs)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComments
        fields = "__all__"

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = "__all__"

class PromotionSerializer(serializers.ModelSerializer):
    # is_active = serializers.BooleanField(read_only=True)
    created_by = serializers.CharField(source='created.username', read_only=True)
    modified_by = serializers.CharField(source='modified.username', read_only=True)
    promoted_products = serializers.SerializerMethodField(method_name='get_promoted_products')
    # image = serializers.ImageField(required=False)

    title_en = serializers.CharField(validators=[validate_slug], write_only=True)
    title_ru = serializers.CharField(validators=[validate_slug], write_only=True)
    title_uz = serializers.CharField(validators=[validate_slug], write_only=True)

    class Meta:
        model = Promotions
        fields = (
            "id", 
            "title","title_uz", "title_ru", "title_en", 
            "percentage", "is_active", 
            'date_from', 'date_till', 
            "created_by", "modified_by", 
            "description", "description_uz", "description_ru", "description_en",
            "products", "promoted_products", 'image', 'imageURL'
            )
        read_only_fields = ['title', 'description', 'imageURL']
        extra_kwargs = {
            "description_uz":{"write_only":True, },
            "description_ru":{"write_only":True, },
            "description_en":{"write_only":True, },
            "title_ru":{"write_only":True, },
            "title_uz":{"write_only":True, },
            "title_en":{"write_only":True, },
            "products":{"write_only":True, },
            "image":{ "read_only":False, },
        }

    def create(self, validated_data):
        promotion = super().create(validated_data)
        if promotion:
            promotion.created = self.context['request'].user
            promotion.save()
        return promotion

    def update(self, instance, validated_data):
        promotion = super().update(instance, validated_data)
        if promotion:
            promotion.modified = self.context['request'].user
            promotion.save()
        return promotion

    def get_promoted_products(self, obj):
        res = ProductsListSerializer(obj.products.all(), many=True).data
        return res
        

class PromotionUpdateSerializer(serializers.Serializer):
    ACTIONS = (
        ('add', _('ADD')),
        ('remove', _('REMOVE')),
    )
    product = serializers.CharField()
    action = serializers.ChoiceField(choices=ACTIONS)

    def create(self, validated_data):
        return None

    def update(self, instance, attrs):
        product_obj = get_object_or_404(Products, slug=attrs['product'])
        action = attrs.pop('action')

        try:
            if action == 'add':
                instance.products.add(product_obj)
            elif action == 'remove':
                instance.products.remove(product_obj)
            instance.modified = self.context['request'].user
            instance.save()
            return instance
        except Exception as e:
            raise e
        
    def to_representation(self, instance):
        return {'detail':'Completed'}



class ContactsSerializer(serializers.ModelSerializer):
    fileURL = serializers.CharField(read_only=True)
    class Meta:
        model = Contacts
        exclude = ('status', )
    def create(self, attrs):
        attrs['status'] = Contacts.SEEN
        return super().create(attrs)

class ContactsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('status', )