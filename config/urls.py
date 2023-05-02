"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from amuzeshyar import views as v
from .views import home

urlpatterns = [
    path('',home),
    path('admin/', admin.site.urls),
    path('edu/api/v1/', include("amuzeshyar.urls")),
    path('edu/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('edu/api/schema/swaggerui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("forms/person/<int:id>", v.load_person_form ),
    path("forms/person/", v.person_form ),
    path('forms/fixedtuition/<int:id>', v.fixed_tuition_edit_form),
    path('forms/fixedtuition/', v.fixed_tuition_form),
    
]
