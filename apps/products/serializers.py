from rest_framework import serializers

from rest_framework.generics import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import *
from .validators import validate_slug


class PromotionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotions
        fields = ("id", "title", "percentage", "is_active", )

    extra_kwargs = {
        "date_from":{"write_only":True, },
        "date_till":{"write_only":True, }
    }


class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ("id", 'image', "imageURL",) #

        read_only_fields = ('imageURL', ) 
        extra_kwargs = {
            'image':{'write_only': True}
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None 
            # or
            # data['imageURL'] = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        
        return data


class ProductsListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(read_only=True, many=False)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ("slug", "title", "status", "price", "price_UZS", "comments_count", "in_promotion", "thumbnail", "seen", "description")

    def get_thumbnail(self, instance):
        if instance.thumbnail:
            return ProductImagesListSerializer(instance.thumbnail, many=False, context=self.context).data


class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ("slug", "title", 'imageURL')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'] and self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None
            # or
            # data['imageURL'] = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        return data


class SubcategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.title", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = SubCategories
        fields = ("slug", "title", "title_en", "title_ru", "title_uz", "category", "products", "category_name", "category_slug", "image", "imageURL")
        read_only_fields = ('title', "imageURL")
        extra_kwargs = {
            'title_en': {'write_only':True, 'required':True},
            'title_ru': {'write_only':True, 'required':True},
            'title_uz': {'write_only':True, 'required':True},
            'category': {'write_only':True, 'required':True},
            'image': {'write_only':True},
        }
    
    def get_products(self, obj):
        return ProductsListSerializer(obj.products.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None
            # or
            # data['imageURL'] = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        return data


class CategoryListCreateSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
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

    def get_subcategories(self, instance):
        return SubcategoryListSerializer(instance.subcategories, read_only=True, many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None
            # or
            # data['imageURL'] = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        return data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    imageURL = serializers.CharField(read_only=True)
    title_en = serializers.CharField(validators=[validate_slug])
    title_ru = serializers.CharField(validators=[validate_slug])
    title_uz = serializers.CharField(validators=[validate_slug])
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

    def get_subcategories(self, instance):
        return SubcategoryListSerializer(instance.subcategories, many=True, context=self.context).data

    def get_products(self, instance):
        return ProductsListSerializer(instance.products, many=True, context=self.context).data
        

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None
            # or
            # data['imageURL'] = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        return data


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComments
        fields = ("id", "name", "review", "comment", )


class ProductSerializer(serializers.ModelSerializer):
    comments = CommentsListSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(many=False, read_only=True)
    images = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.title",read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    subcategory_name = serializers.CharField(source="sub_category.title",read_only=True)
    subcategory_slug = serializers.CharField(source="sub_category.slug", read_only=True)

    similar_products = serializers.SerializerMethodField()
    
    title_en = serializers.CharField(validators=[validate_slug])
    title_ru = serializers.CharField(validators=[validate_slug])
    title_uz = serializers.CharField(validators=[validate_slug])

    class Meta:
        model = Products
        fields = (
            "slug", "title", "title_en","title_ru", "title_uz",
            "category", "category_name", "category_slug",
            "sub_category", "subcategory_name", "subcategory_slug",
            "description_en", "description_ru","description_uz", "characteristics_en", "characteristics_ru", "characteristics_uz", 'status', 'price', 'quantity',
            'comments', 'comments_count', 'in_promotion','similar_products',
            'images', 'seen', 'description', 
            'price_UZS',
        )
        read_only_fields = [
             'title', "description", "characteristics",'seen', 'slug', 'price_UZS'
            ]

    def create(self, attrs):
        product = super().create(attrs)
        product.created = self.context['request'].user
        product.save()
        
        return product

    def get_images(self, instance):
        return ProductImagesListSerializer(instance.images, many=True, context=self.context).data

    def get_similar_products(self, instance):
        return ProductsListSerializer(instance.similar_products, many=True, context=self.context).data


class ProductUpdateSerializer(serializers.ModelSerializer):
    title_en = serializers.CharField(validators=[validate_slug])
    title_ru = serializers.CharField(validators=[validate_slug])
    title_uz = serializers.CharField(validators=[validate_slug])

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['image'].replace('http', 'https') if data['image'] is not None else None
        
        return data

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

    title_en = serializers.CharField(validators=[validate_slug])
    title_ru = serializers.CharField(validators=[validate_slug])
    title_uz = serializers.CharField(validators=[validate_slug])

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
            # "description_uz":{"write_only":True, },
            # "description_ru":{"write_only":True, },
            # "description_en":{"write_only":True, },
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
        res = ProductsListSerializer(obj.products.all(), many=True, context=self.context).data
        return res

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['imageURL'] = data['imageURL'].replace('http', 'https') if data['imageURL'] is not None else None
        
        return data    

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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].scheme == 'https':
            data['fileURL'] = data['fileURL'].replace('http', 'https') if data['fileURL'] is not None else None
        
        return data

class ContactsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('status', )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'value', )
