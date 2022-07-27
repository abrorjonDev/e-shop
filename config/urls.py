"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as drf_get_schema_view# new
from drf_yasg import openapi # new
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions 

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https"]
        return schema

schema_view = drf_get_schema_view( # new
    openapi.Info(
        title="E-shop API",
        url='https://shop.abrorjonaxmadov.uz/',
        default_version="v1",
        description="API for E-shop",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="pro.akhmadov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
        public=True,
        generator_class=BothHttpAndHttpsSchemaGenerator, # Here
        permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)


urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('api/v1/', include('apps.products.urls')),
    path('api/v1/', include('apps.accounts.urls')),
    path('auth/v1/', include('dj_rest_auth.urls')),
    path('auth/v1/registration', include('dj_rest_auth.registration.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('openapi/', get_schema_view(
            title="E-shop",
            description="E-shop API with Django",
            version="1.0.0"
        ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='docs/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),

    path('', schema_view.with_ui( # new
    'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui( # new
    'redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
