
from django.urls import path


from amuzeshyar import apis as a
from amuzeshyar import views as v

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

    # Building
    path('api/v1/buildings/', a.Building.as_view()),

    # Room
    path('api/v1/rooms/', a.Room.as_view()),

    # Department
    path('api/v1/departments/', a.DepartmentList.as_view()),
    path('api/v1/departments/<int:pk>', a.DepartmentDetail.as_view()),

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
    path('api/v1/ann', a.Announcement.Announcement_List_detail),
    path('api/v1/ann/', a.Announcement.as_view()),
    path('api/v1/ann/<int:id>', a.Announcement.as_view()),
    # AnnouncementText
    path('api/v1/anntext', a.AnnouncementText.Announcement_List_detail),
    path('api/v1/anntext/', a.AnnouncementText.as_view()),
    path('api/v1/anntext/<int:id>', a.AnnouncementText.as_view()),

    # Semester
    path('api/v1/coursetuitions', a.Semester.Semester_List_detail),
    path('api/v1/coursetuitions/', a.Semester.as_view()),
    path('api/v1/coursetuitions/<int:id>', a.Semester.as_view()),
    
    path('api/v1/panel/<int:student_id>',a.first_page )
]
# Rendered Pages
urlpatterns += [
    path('<int:student_id>', v.home),

]
# Forms
urlpatterns += [
    path("forms/person/<int:id>", v.load_person_form),
    path("forms/person", v.person_form),
    path('forms/fixedtuition/<int:id>', v.fixed_tuition_edit_form),
    path('forms/fixedtuition', v.fixed_tuition_form),
    path('forms/studentclass/<int:id>', v.student_class_edit_form),
    path('forms/studentclass', v.student_class_form),
    path('forms/classattendance/<int:id>', v.class_attendance_edit_form),
    path('forms/classattendance', v.class_attendance_form),
]


