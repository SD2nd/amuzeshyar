
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from amuzeshyar import apis as a
from amuzeshyar import views as v

app_name = "amuzeshyar"
# APIS
urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swaggerui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
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

    # classAttendance
    path('api/v1/classAttendances/', a.ClassAttendance_List,
         name="get_class_attenndanceList"),
    path('api/v1/classAttendances/<int:id>', a.ClassAttendance_List_detail),

    # studentClass
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
    path('api/v1/fixedfees', a.FixedTuitionFee.FixedTuitionFee_List_detail),
    path('api/v1/fixedfees/', a.FixedTuitionFee.as_view()),
    path('api/v1/fixedfees/<int:id>', a.FixedTuitionFee.as_view()),

    # SemesterCourseTuition
    path('api/v1/coursetuitions',
         a.SemesterCourseTuition.SemesterCourseTuition_List_detail),
    path('api/v1/coursetuitions/', a.SemesterCourseTuition.as_view()),
    path('api/v1/coursetuitions/<int:id>', a.SemesterCourseTuition.as_view()),

    # StudentInvoice
    path('api/v1/invoices', a.StudentInvoice.StudentInvoice_List_detail),
    path('api/v1/invoices/', a.StudentInvoice.as_view()),
    path('api/v1/invoices/<int:id>', a.StudentInvoice.as_view()),

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
    path('api/v1/coursetuitions/<int:id>', a.Semester.as_view())
]
# Rendered Pages
urlpatterns += [
    path('', v.home),

]
# Forms
urlpatterns += [
    path("forms/person/<int:id>", v.load_person_form),
    path("forms/person", v.person_form),
    path('forms/fixedtuition/<int:id>', v.fixed_tuition_edit_form),
    path('forms/fixedtuition', v.fixed_tuition_form),
]
