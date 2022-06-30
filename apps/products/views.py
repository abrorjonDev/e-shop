from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


# INTERNALS
from .models import *
from .serializers import *


class CategoryListView(generics.ListCreateAPIView):
    
    """
        Methods you can call here: `GET`, `POST`\n
        `GET` method is open to any user (for client and admins), however\n
        `POST` method requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """
    
    queryset = Categories.objects.all()
    serializer_class = CategoryListCreateSerializer

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


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    """
        Methods you can call here: `GET`, `PUT`, `PATCH`, `DELETE` \n
        `GET` method is open to any user (for client and admins), however\n
        Other methods requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """

    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def put(self, request, slug):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, 
            data=request.data, 
            partial=True, 
            context={"request": request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, slug):
        return self.put(request, slug)

    # DON'T NEED OVERRIDE
    # def delete(self, request, slug):
    #    pass      


class SubCategoryListView(generics.ListCreateAPIView):
    
    """
        Methods you can call here: `GET`, `POST`\n
        `GET` method is open to any user (for client and admins), however\n
        `POST` method requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """
    
    queryset = SubCategories.objects.all()
    serializer_class = SubcategorySerializer

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


class SubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    """
        Methods you can call here: `GET`, `PUT`, `PATCH`, `DELETE` \n
        `GET` method is open to any user (for client and admins), however\n
        Other methods requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """

    queryset = SubCategories.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'

    def put(self, request, slug):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, 
            data=request.data, 
            partial=True, 
            context={"request": request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, slug):
        return self.put(request, slug)

    # DON'T NEED OVERRIDE
    # def delete(self, request, slug):
    #    pass      


class ProductListCreateView(generics.ListCreateAPIView):
    
    """
        Methods you can call here: `GET`, `POST`\n
        `GET` method is open to any user (for client and admins), however\n
        `POST` method requires authentication.
        For this, you need to add headers this:
            `Authorization`: `Token <user token key from succesfull login response>` 
        
        For getting content in any language, you need to add to headers:
            `Accept-Language`: `en` (or `ru`)
    """

    queryset = Products.objects.all()
    serializer_class = ProductsListSerializer
    
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
    queryset = SubCategories.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'

    def put(self, request, slug):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, 
            data=request.data, 
            partial=True, 
            context={"request": request}
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, slug):
        return self.put(request, slug)

    # DON'T NEED OVERRIDE
    # def delete(self, request, slug):
    #    pass      

