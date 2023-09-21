from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Album API",
        default_version="v1",
        description="Album API built by javid.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mohammadrezajavid3@gmail.com"),
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url="http://127.0.0.1:8000/",
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('auth/', include('authentication.urls')),
    path('api/v1/', include('albumApp.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
