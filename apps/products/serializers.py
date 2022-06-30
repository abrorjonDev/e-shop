from rest_framework import serializers



from .models import *



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
    in_promotion = PromotionListSerializer(required=False, many=False)
    thumbnail = ProductImagesListSerializer(required=False, many=False)
    images = serializers.FileField(write_only=True)
    class Meta:
        model = Products
        fields = ("slug", "title", "status", "price", "comments_count", "in_promotion", "thumbnail", "images", "seen")

    

class SubcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ("slug", "title")


class SubcategorySerializer(serializers.ModelSerializer):
    # products = ProductsListSerializer(required=False, many=True)
    products = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.title",required=False)
    category_slug = serializers.CharField(source="category.slug", required=False)
    class Meta:
        model = SubCategories
        fields = ("slug", "title", "title_en", "title_ru", "title_uz", "category", "products", "category_name", "category_slug")
        read_only_fields = ('title', "category_name", "category_slug")
        write_only_fields = ["title_en","title_ru", "title_uz"]


        # kwargs = {
        #     'title_en':{'write_only':True},
        #     'title_ru':{'write_only':True},
        #     'title_uz':{'write_only':True},
        # }
    
    def get_products(self, obj):
        response = ProductsListSerializer(obj.products.all(), many=True).data
        return response


class CategoryListCreateSerializer(serializers.ModelSerializer):
    subcategories = SubcategoryListSerializer(required=False, many=True)
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Categories
        fields = ("slug", "title", "title_en","title_ru", "title_uz", "subcategories")
        read_only_fields = ('title', )
        write_only_fields = ["title_en","title_ru", "title_uz"]
        
        # kwargs = {
        #     'slug':{'read_only':True, }
        # }

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
    subcategories = SubcategoryListSerializer(required=False, many=True)
    products = ProductsListSerializer(required=False, many=True)

    class Meta:
        model = Categories
        fields = ("slug", "title","title_en","title_ru", "title_uz","subcategories", "products")
        read_only_fields = ['slug', "subcategories", "products", 'title']
        write_only_fields = ["title_en","title_ru", "title_uz"]

    def update(self, instance, attrs):
        instance.modified = self.context['request'].user
        return super().update(instance, attrs)


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComments
        fields = ("id", "name", "review", "comment", )

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentsListSerializer(required=False, many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    in_promotion = PromotionListSerializer(many=False, read_only=True)
    images = ProductImagesListSerializer(required=False, many=True)
    # files = serializers.FileField(write_only=True)
    category_name = serializers.CharField(source="category.title",read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    subcategory_name = serializers.CharField(source="sub_category.title",read_only=True)
    subcategory_slug = serializers.CharField(source="sub_category.slug", read_only=True)

    similar_products = ProductsListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Products
        fields = (
            "slug", "title", "title_en","title_ru", "title_uz",
            "category", "category_name", "category_slug",
            "sub_category", "subcategory_name", "subcategory_slug",
            "description_en", "description_ru","description_uz", "characteristics_en", "characteristics_ru", "characteristics_uz", 'status', 'price', 'quantity',
            'comments', 'comments_count', 'in_promotion','similar_products',
            'images', 'seen'
        )
        read_only_fields = ['slug',  'category_name', 'category_slug', 'subcategory_name', 'subcategory_slug',
            'comments', 'comments_count', 'title', "description", "characteristics",
            'in_promotion','similar_products','seen'
            ]
        write_only_fields = [
            "title_en","title_ru", "title_uz",
            "description_en", "description_ru","description_uz",
            "characteristics_en", "characteristics_ru", "characteristics_uz",
        ]

    def create(self, attrs):
        images = self.context['request'].FILES.pop('files')
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

