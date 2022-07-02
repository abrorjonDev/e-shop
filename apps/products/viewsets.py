
from rest_framework import viewsets

# INTERNALS
from .models import *
from .serializers import *
from .filters import *

class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ProductCommentsViewSet(viewsets.ModelViewSet):
    queryset = ProductComments.objects.all()
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class PromotionViewSet(viewsets.ModelViewSet):
    """All promotions here.."""
    queryset = Promotions.objects.all()
    serializer_class = PromotionSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['salom'] = 'text'
    #     print("CONTEXT: ", context)
    #     return context


class PromotionProductAddRemoveViewSet(viewsets.ModelViewSet):
    """
    You can add product or remove product from promotion.
    """

    queryset = Promotions.objects.all()
    serializer_class = PromotionUpdateSerializer
    http_method_names = ['retrieve', 'patch']

    # def retrieve(self, request, *args, **kwargs):
