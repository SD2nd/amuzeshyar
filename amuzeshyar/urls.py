
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
    path('persons/', a.PersonList.as_view(), name= "create_list_all_person"),
    path('persons/<str:national_id>', a.PersonDetail.as_view(), name= "get_edit_delete_person"),
    
    # student
    path('students/', a.StudentList.as_view(), name= "create_list_all_student"),
    path('students/<int:student_id>', a.StudentDetail.as_view(), name= "get_edit_delete_student"),

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
    path('departments/', a.DepartmentList.as_view()),
    path('departments/<int:pk>', a.DepartmentDetail.as_view()),
    

    #FixedTuitionFee
    path('fixedfees', a.FixedTuitionFee.FixedTuitionFee_List_detail),
    path('fixedfees/', a.FixedTuitionFee.as_view()),
    path('fixedfees/<int:id>', a.FixedTuitionFee.as_view()),

    #SemesterCourseTuition
    path('coursetuitions', a.SemesterCourseTuition.SemesterCourseTuition_List_detail),
    path('coursetuitions/', a.SemesterCourseTuition.as_view()),
    path('coursetuitions/<int:id>', a.SemesterCourseTuition.as_view()),

    #StudentInvoice
    path('invoices', a.StudentInvoice.StudentInvoice_List_detail),
    path('invoices/', a.StudentInvoice.as_view()),
    path('invoices/<int:id>', a.StudentInvoice.as_view()),

    #constvalues
    path('constvalues/', a.ConstValueList.as_view(), name= "create_list_all_constvalue"),
    path('constvalues/<int:pk>', a.ConstValueDetail.as_view(), name= "get_put_patch_delete_constvalue"),

    #Semester
    path('coursetuitions', a.Semester.Semester_List_detail),
    path('coursetuitions/', a.Semester.as_view()),
    path('coursetuitions/<int:id>', a.Semester.as_view()),

]
