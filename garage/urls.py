from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/users/', include('users.urls')),
]

# Swagger
urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("swagger/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
