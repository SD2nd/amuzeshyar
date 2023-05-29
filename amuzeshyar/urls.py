from django.urls import path


from amuzeshyar import apis as a
from amuzeshyar import views as v

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "amuzeshyar"
# APIS
urlpatterns = [

    # person
    path('api/v1/persons/', a.PersonList.as_view(),
         name="create_list_all_person"),
    path('api/v1/persons/<str:national_id>',
         a.PersonDetail.as_view(), name="get_edit_delete_person"),

    # student
    path('api/v1/students/', a.StudentList.as_view(),
         name="create_list_all_student"),
    path('api/v1/students/<int:student_id>',
         a.StudentDetail.as_view(), name="get_edit_delete_student"),

    # classAttendance not ok
    path('api/v1/classAttendances/', a.ClassAttendance_List,
         name="get_class_attenndanceList"),
    path('api/v1/classAttendances/<int:id>', a.ClassAttendance_List_detail),

    # Specialization
    path('api/V1/Specialization', a.Specialization.as_view()),


    # studentClass not ok
    path('api/v1/studentClass/', a.StudentClass_list,
         name="get_class_attenndanceList"),
    path('api/v1/studentClass/<int:id>', a.StudentClass_List_detail),

    # Course
    path('api/v1/Course/', a.Course_list.as_view(),
         name="get_class_attenndanceList"),
     
     path('api/v1/Course/<int:pk>', a.CourseDetail.as_view(),
         name="get_class_attenndanceList"), 

    # Building
    path('api/v1/buildings/', a.Building.as_view()),
    path('api/v1/buildings/<int:id>', a.Building_List_detail),

    # Room
    path('api/v1/rooms/', a.Room.as_view()),
    path('api/v1/rooms/<str:code>', a.Room_List_detail),

    # Department
    path('api/v1/departments/', a.Department_list.as_view()),
    path('api/v1/departments/<int:id>', a.Department_List_detail),

    # FixedTuitionFee
    path('api/v1/fixedfees/', a.FixedTuitionFee_List),
    path('api/v1/fixedfees/<int:id>', a.FixedTuitionFee_Detail),

    # SemesterCourseTuition,
    path('api/v1/coursetuitions/', a.SemesterCourseTuition_List),
    path('api/v1/coursetuitions/<int:id>', a.SemesterCourseTuition_Detail),

    # StudentInvoice
    path('api/v1/invoices/', a.StudentInvoice_List),
    path('api/v1/invoices/<int:id>', a.StudentInvoice_Detail),

    # StudentPayment
    path('api/v1/payments/', a.StudentPayment_List),
    path('api/v1/payments/<int:id>', a.StudentPayment_Detail),

    # constvalues
    path('api/v1/constvalues/', a.ConstValueList.as_view(),
         name="create_list_all_constvalue"),
    path('api/v1/constvalues/<int:pk>', a.ConstValueDetail.as_view(),
         name="get_put_patch_delete_constvalue"),

    # Announcement
    path('api/v1/ann/', a.Announcement_List),
    path('api/v1/ann/<int:id>', a.Announcement_Detail),
    # AnnouncementText
    path('api/v1/anntext/', a.AnnouncementText_List),
    path('api/v1/anntext/<int:id>', a.AnnouncementText_Detail),

    # Semester
    path('api/v1/semesters', a.Semester.Semester_List_detail),
    path('api/v1/semesters/', a.Semester.as_view()),
    path('api/v1/semesters/<int:id>', a.Semester.as_view()),
    
    path('api/v1/panel/<int:student_id>',a.first_page ),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# Rendered Pages
urlpatterns += [
    path('<int:student_id>', v.home, name="home"),

]
# Forms
urlpatterns += [
    path("forms/person/<int:id>", v.load_person_form),
    path("forms/person", v.person_form),
    path('forms/fixedfees/<int:id>', v.fixed_tuition_edit_form),
    path('forms/fixedfees', v.fixed_tuition_form),
    path('forms/coursetuitions/<int:id>', v.course_tuition_edit_form),
    path('forms/coursetuitions', v.course_tuition_form),
    path('forms/invoices/<int:id>', v.invoice_edit_form),
    path('forms/invoices', v.invoice_form),
    path('forms/payments/<int:id>', v.payment_edit_form),
    path('forms/payments', v.payment_form),
    path('forms/studentclass/<int:id>', v.student_class_edit_form),
    path('forms/studentclass', v.student_class_form),
    path('forms/classattendance/<int:id>', v.class_attendance_edit_form),
    path('forms/classattendance', v.class_attendance_form),
    path('forms/department', v.department_form),
    path('forms/department/<int:id>', v.department_edit_form),
    path('forms/room', v.room_form),
    path('forms/room/<int:id>', v.room_edit_form),
    path('forms/building', v.building_form),
    path('forms/building/<int:id>', v.building_edit_form),
    path('forms/announcement/<int:id>', v.announcement_edit_form),
    path('forms/announcement', v.announcement_form),
    path("login", v.login_form)

    
]
