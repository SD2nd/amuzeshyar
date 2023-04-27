
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
    path('persons', a.Person.all_persons, name= "all_persons"),
    path('persons/', a.Person.as_view(), name= "create_person"),
    path('persons/<str:national_id>', a.Person.as_view(), name= "get_edit_delete_person"),
    
    # student
    path('students', a.Student.get_students, name= "get_all_students"),
    path('students/', a.Student.as_view(), name= "create_new_student"),
    path('students/<int:student_id>', a.Student.as_view(), name= "get_edit_delete_student"),

    #classAttendance
    path('classAttendances/', a.ClassAttendance_List, name="get_class_attenndanceList"),
    path('classAttendances/<int:id>', a.ClassAttendance_List_detail),

    #studentClass
    path('studentClass/', a.StudentClass_list, name="get_class_attenndanceList"),
    path('studentClass/<int:id>', a.StudentClass_List_detail),
    
    #Course
    path('Course/',a.Course_list.as_view(), name="get_class_attenndanceList"),
  #  path('studentClass/<int:id>', StudentClass_List_detail),

    #Building 
    path('buildings/', a.Building.as_view()),
    
    #Room
    path('rooms/', a.Room.as_view()),

    #Department
    path('departments/', a.Department.as_view()),
    
    #ConstValue    
    path('constvalues/', a.ConstValue.as_view()),
]
