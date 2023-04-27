
from django.urls import path
from amuzeshyar import apis as a
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
    path('api/v1/persons', a.Person.all_persons, name= "all_persons"),
    path('api/v1/persons/', a.Person.as_view(), name= "create_person"),
    path('api/v1/persons/<str:national_id>', a.Person.as_view(), name= "get_edit_delete_person"),
    
    # student
    path('api/v1/students', a.Student.get_students, name= "get_all_students"),
    path('api/v1/students/', a.Student.as_view(), name= "create_new_student"),
    path('api/v1/students/<int:student_id>', a.Student.as_view(), name= "get_edit_delete_student"),

    #classAttendance
    path('api/v1/classAttendances/', a.ClassAttendance_List, name="get_class_attenndanceList"),
    path('api/v1/classAttendances/<int:id>', a.ClassAttendance_List_detail),

    #studentClass
    path('api/v1/studentClass/', a.StudentClass_list, name="get_class_attenndanceList"),
    path('api/v1/studentClass/<int:id>', a.StudentClass_List_detail),
    
    #Course
    path('api/v1/Course/',a.Course_list.as_view(), name="get_class_attenndanceList"),
  #  path('api/v1/studentClass/<int:id>', StudentClass_List_detail),


]
