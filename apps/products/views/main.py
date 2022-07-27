from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters import rest_framework as rf_filter

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# INTERNALS
from ..models import *
from ..serializers import *
from ..filters import *

class CategoryBaseClass:
    queryset = Categories.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryListView(CategoryBaseClass, generics.ListAPIView):
    
    """
        Methods you can call here: `GET`, `POST`\n
        `GET` method is open to any user (for client and admins), however\n
        `POST` method requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """
    
    filter_backends = [rf_filter.DjangoFilterBackend, ]
    filterset_class = CategoryFilterSet


class CategoryCreateAPIView(CategoryBaseClass, generics.CreateAPIView):
    """Create API View"""
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(CategoryBaseClass, generics.RetrieveAPIView):
    """
        For Authentication, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """

    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryUpdateAPIView(CategoryBaseClass, generics.UpdateAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CategoryDeleteAPIView(CategoryBaseClass, generics.DestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'slug'

###########################################################################################

class SubCategoryBaseClass:
    queryset = SubCategories.objects.all()
    serializer_class = SubcategorySerializer


class SubCategoryListView(SubCategoryBaseClass, generics.ListAPIView):
    
    """
    Sub Categories List APIView.
    """
    filter_backends = [rf_filter.DjangoFilterBackend, ]
    filterset_fields = ['title', 'category__title', 'category__slug']
    

class SubCategoryCreateAPIView(SubCategoryBaseClass, generics.CreateAPIView):
    """ Sub Category Create API View. """
    pass


class SubCategoryDetailView(SubCategoryBaseClass, generics.RetrieveAPIView):
    
    """
        For Authorization, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """
    lookup_field = 'slug'


class SubcategoryUpdateAPIView(SubCategoryBaseClass, generics.UpdateAPIView):
    lookup_field = 'slug'
 

class SubcategoryDeleteAPIView(SubCategoryBaseClass, generics.DestroyAPIView):
    lookup_field = 'slug'


class ProductListCreateView(generics.ListCreateAPIView):
    
    """
        Methods you can call here: `GET`, `POST`\n
        `GET` method is open to any user (for client and admins), however\n
        `POST` method requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)

        IN Post:
            {
               "title": "",\n
               "status": null,\n
               "price": null,\n
               "images": null\n
            }
        
        Add `files` to your request for posting product with it's images. 
    """
    filter_backends = [rf_filter.DjangoFilterBackend, ]
    filterset_class = ProductFilterSet
    queryset = Products.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializer
        else:
            return self.serializer_class
    
    serializer_class = ProductsListSerializer

    @swagger_auto_schema(request_body=ProductSerializer,  response={201:ProductsListSerializer})
    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(
            data=request.data, 
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
        Methods you can call here: `GET`, `PUT`, `PATCH`, `DELETE` \n
        `GET` method is open to any user (for client and admins), however\n
        Other methods requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        else:
            return self.serializer_class
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.seen = instance.seen+1 
            instance.save()
        serializer = self.get_serializer(instance, many=False)
        return super().get(request, *args, **kwargs)

    def put(self, request, slug):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True, 
            context={"request": request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return self.get(request, slug=slug) # Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, slug):
        return self.put(request, slug)

    # DON'T NEED OVERRIDE
    # def delete(self, request, slug):
    #    pass      


class PromotionBaseView:
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer


class PromotionListAPIView(PromotionBaseView, generics.ListAPIView):
    """Promotion List API."""


class PromotionCreateAPIView(PromotionBaseView, generics.CreateAPIView):
    """Promotion Create API."""


class PromotionRetrieveAPIView(PromotionBaseView, generics.RetrieveAPIView):
    """Promotion Retrieve API."""

    lookup_field = 'id'


class PromotionUpdateAPIView(PromotionBaseView, generics.UpdateAPIView):
    """Promotion Update API."""
    lookup_field = 'id'


class PromotionDeleteAPIView(PromotionBaseView, generics.DestroyAPIView):
    """Promotion Delete API."""
    lookup_field = 'id'


class PromotionAddRemoveAPIView(PromotionBaseView, generics.UpdateAPIView):
    """You can add or remove products from promotion.."""
    serializer_class = PromotionUpdateSerializer