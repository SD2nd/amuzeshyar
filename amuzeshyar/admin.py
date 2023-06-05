from django.contrib import admin
from amuzeshyar import models as m

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "national_id", "role")
    list_filter = ("role",)
    search_fields = ("first_name", "last_name")


class FixedTuitionAdmin(admin.ModelAdmin):
    list_display = ("id", "semester", "fee", "field_of_study")
    list_filter = ("year",)
    search_fields = ("field_of_study",)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("datetime", "semester", "is_succeeded", "invoice", "student")
    list_filter = ("datetime", )
    search_fields = ("student", "datetime", "invoice",)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "creation_date", "is_payed", "indebtedness", "semester_id", "student_id")
    list_filter = ("creation_date", "description")
    search_fields = ("creation_date", "student_id")


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("announcement", "specific_major", "specific_specialization", "specific_student", "create_datetime",
                    "specific_department")
    list_filter = ("create_datetime", "specific_department", "specific_major", "specific_specialization")
    search_fields = ("create_datetime", "announcement", "specific_department", "specific_major", "specific_specialization")


class SemesterAdmin(admin.ModelAdmin):
    list_display = ("semester_code","semester_type", "registration_start_date", "year" )
    list_filter = ("year",)
    search_fields = ["year"]

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title","english_title","major")
    list_filter = ("major",)
    search_fields = ("title",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("person","entry_semester","field_of_study")


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("person","academic_rank")


class ClassAdmin(admin.ModelAdmin):
    list_display = ("course","instructor","semester" ,"capacity")

class ClassscheduelAdmin(admin.ModelAdmin):
    list_display = ("session","روزهای_هفته","location")


class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("student","session","grade", "is_active", "semester")
    
    def semester(self, obj):
        return obj.session.semester


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title","degree_level")


class SemesterCourseTuitionAdmin(admin.ModelAdmin):
    list_display = ("semester","field_of_study", "course_type", "unit_type", "tuition_per_unit",)

class ClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ("session_number","session","student")

class CoursePreReqAdmin(admin.ModelAdmin):
    list_display = ("c1", "is_prerequisite","is_concurrent","c2")
    
admin.site.register(m.FixedTuitionFee, FixedTuitionAdmin)
admin.site.register(m.Person, PersonAdmin)
admin.site.register(m.Student, StudentAdmin)
admin.site.register(m.Department)
admin.site.register(m.Room)
admin.site.register(m.Major)
admin.site.register(m.Semester,SemesterAdmin)
admin.site.register(m.Specialization, SpecializationAdmin)
admin.site.register(m.Building)
admin.site.register(m.Professor, ProfessorAdmin)
admin.site.register(m.Course, CourseAdmin)
admin.site.register(m.Class, ClassAdmin)
admin.site.register(m.Announcement,AnnouncementAdmin)
admin.site.register(m.AnnouncementText)
admin.site.register(m.SemesterCourseTuition, SemesterCourseTuitionAdmin)
admin.site.register(m.ClassAttendance, ClassAttendanceAdmin)
admin.site.register(m.StudentClass, StudentClassAdmin)
admin.site.register(m.StudentInvoice, InvoiceAdmin)
admin.site.register(m.ClassSchedule,ClassscheduelAdmin)
admin.site.register(m.StudentPayment, PaymentAdmin)
admin.site.register(m.CoursePrerequisite, CoursePreReqAdmin)






