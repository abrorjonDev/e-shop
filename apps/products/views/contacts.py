from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.permissions import AllowAny


from ..models import Contacts
from ..serializers import ContactsSerializer, ContactsUpdateSerializer
from ..filters import ContactsFilter
class ContactsBaseView:
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class ContactsListAPIView(ContactsBaseView, ListAPIView):
    """Contacts List API."""

    filter_backends = [DjangoFilterBackend]
    filterset_class = ContactsFilter


class ContactsCreateAPIView(ContactsBaseView, CreateAPIView):
    """Contacts Create API.
    
    Bunda aslida `file` ham bor. Agar mijoz file jo'natmoqchi bo'lsa.  
    """
    permission_classes = (AllowAny, )


class ContactsRetrieveAPIView(ContactsBaseView,RetrieveAPIView):
    """Contacts Retrieve API."""
    lookup_field = 'id'


class ContactsUpdateAPIView(ContactsBaseView, UpdateAPIView):
    """Contacts Update API."""
    lookup_field = 'id'
    serializer_class = ContactsUpdateSerializer


class ContactsDeleteAPIView(ContactsBaseView, DestroyAPIView):
    """Contacts Delete API."""
    lookup_field = 'id'