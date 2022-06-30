from rest_framework import serializers



from .models import *



class PromotionListSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, many=False)
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
        fields = ("id", "imageURL", 'image')

    extra_kwargs = {
        'image': {
            "write_only":True, "required":False
        }
    }

class ProductsListSerializer(serializers.ModelSerializer):
    
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(required=False, many=False)
    thumbnail = ProductImagesListSerializer(required=False, many=False)
    images = serializers.FileField(write_only=True, many=True)
    class Meta:
        model = Products
        fields = ("slug", "title", "status", "price", "comments_count", "in_promotion", "thumbnail")

    def create(self, attrs):
        images = attrs.pop('images')
        product = super().create(attrs)
        product.created = self.context['request'].user
        product.save()
        for img in images:
            ProductImages.objects.create(
                image=img,
                product=product,
                created=product.created
            )
        return product

class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ("slug", "title")


class SubcategorySerializer(serializers.ModelSerializer):
    products = ProductsListSerializer(required=False, many=True)
    category_name = serializers.CharField(source="category.title",required=False, many=False)
    category_slug = serializers.CharField(source="category.slug", required=False, many=False)
    class Meta:
        model = SubCategories
        fields = ("slug", "title", "category", "products", "category_name", "category_slug")


class CategoryListCreateSerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(required=False, many=True)

    class Meta:
        model = Categories
        fields = ("slug", "title", "subcategories")

    extra_kwargs = {
        'slug':{'read_only':True, }
    }

    def create(self, attrs):
        category = self._meta.model(
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
    subcategories = SubcategoryListSerializer(required=False, many=True)
    products = ProductsListSerializer(required=False, many=True)

    class Meta:
        model = Categories
        fields = ("slug", "title","subcategories", "products")

    def update(self, instance, attrs):
        instance.modified = self.context['request'].user
        return super().update(instance, attrs)


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComments
        fields = ("id", "name", "review", "comment", )

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentsListSerializer(required=False, many=True)
    comments_count = serializers.PositiveIntegerField(required=False, many=False)
    in_promotion = PromotionListSerializer(required=False, many=False)
    images = ProductImagesListSerializer(required=False, many=True)
    
    category_name = serializers.CharField(source="category.title",required=False, many=False)
    category_slug = serializers.CharField(source="category.slug", required=False, many=False)

    subcategory_name = serializers.CharField(source="sub_category.title",required=False, many=False)
    subcategory_slug = serializers.CharField(source="sub_category.slug", required=False, many=False)

    similar_products = ProductsListSerializer(many=True, required=False)
    
    class Meta:
        model = Products
        fields = (
            "slug", "title", 
            "category", "category_name", "category_slug",
            "sub_category", "subcategory_name", "subcategory_slug",
            "description", "characteristics", 'status', 'price', 'quantity',
            'comments', 'comments_count', 'in_promotion','similar_products',
            'images',
        )

    





