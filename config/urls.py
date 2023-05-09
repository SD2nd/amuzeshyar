from django.contrib import admin
from django.urls import path, include

from amuzeshyar import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('edu/', include("amuzeshyar.urls")),
]
