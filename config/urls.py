from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from amuzeshyar import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('edu/', include("amuzeshyar.urls")),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swaggerui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
