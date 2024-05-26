
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from server import views
from django.conf import settings
from django.conf.urls.static import static
# Server Urls end endpoints

router = routers.DefaultRouter()
# router.register(
#     r'api', views., basename='allproducts'
# )
# router.register(r'api/server/select/(?P<category>[^/.]+)', views.ServerListView,
#                 basename='server_category')

router.register(r'api/server/select', views.ServerListView,
                basename='server_category')


# Drf Ysag Views For api Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="ChattApp Api ",
        default_version='v1',
        description="This is Chatt App  api using django rest fraemwork ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('api/api.json/', schema_view.without_ui(
         cache_timeout=0), name='schema-swagger-ui-no'),
    path('api/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]+router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
