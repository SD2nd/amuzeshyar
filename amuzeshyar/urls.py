
from django.urls import path
from .apis import Person, register_student
# config URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

app_name = "amuzeshyar"
urlpatterns = [
    path('api/v1/persons/<str:national_id>', Person.as_view(), name= "post_person_information"),
    
    path('api/v1/persons/', Person.as_view(), name= "post_person_information"),
    path('api/v1/student/', register_student, name= "full-info-person_information"),
    
    # path('api/v1/persons/<str:national_id>', get_by_national_id),
    # path('api/v1/persons/<str:national_id>/del', del_person),
    

]
