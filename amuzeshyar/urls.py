
from django.urls import path
from .apis import Person, Student, ClassAttendance_List, ClassAttendance_List_detail, StudentClass_list, StudentClass_List_detail , Specialization

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
    # person
    path('api/v1/persons', Person.all_persons, name= "all_persons"),
    path('api/v1/persons/', Person.as_view(), name= "create_person"),
    path('api/v1/persons/<str:national_id>', Person.as_view(), name= "get_edit_delete_person"),
    
    # student
    path('api/v1/students', Student.get_students, name= "get_all_students"),
    path('api/v1/students/', Student.as_view(), name= "create_new_student"),
    path('api/v1/students/<int:student_id>', Student.as_view(), name= "get_edit_delete_student"),

    #classAttendance
    path('api/v1/classAttendances/', ClassAttendance_List, name="get_class_attenndanceList"),
    path('api/v1/classAttendances/<int:id>', ClassAttendance_List_detail),

    #studentClass
    path('api/v1/studentClass/', StudentClass_list, name="get_class_attenndanceList"),
    path('api/v1/studentClass/<int:id>', StudentClass_List_detail),

    path('api/v1/SpecializationClass/', Specialization.as_view(), name="get_class_attenndanceList"),

]
