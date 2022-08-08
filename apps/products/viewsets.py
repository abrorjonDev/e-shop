from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
# INTERNALS
from .models import *
from .serializers import *
from .filters import *

class ProductImagesViewSet(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer
    parser_classes = (FormParser, MultiPartParser)
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # context['request'] = self.request
        print("CONTEXT: ", context)
        return context


class PromotionProductAddRemoveViewSet(viewsets.ModelViewSet):
    """
    You can add product or remove product from promotion.
    """

    queryset = Promotions.objects.all()
    serializer_class = PromotionUpdateSerializer
    http_method_names = ['retrieve', 'patch']

    # def retrieve(self, request, *args, **kwargs):


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    Only get the last currency value
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


    def list(self, request, *args, **kwargs):
        last_obj = Currency.objects.last()
        return Response(self.serializer_class(last_obj, many=False).data, status=200)