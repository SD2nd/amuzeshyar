from django.contrib import admin
from amuzeshyar import models as m

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "national_id", "role")
    list_filter = ("role",)
    search_fields = ("first_name", "last_name")

class FixedTuitionAdmin(admin.ModelAdmin):
    list_display = ("id", "semester", "field_of_study")
    list_filter = ("year",)
    search_fields = ("field_of_study",)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("semester_type", "registration_start_date", "year" )
    list_filter = ("year",)
    #search_fields = ("semester_type")

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("title","english_title","major")
    list_filter = ("major",)
    search_fields = ("title",)


admin.site.register(m.FixedTuitionFee, FixedTuitionAdmin)
admin.site.register(m.Person, PersonAdmin)
admin.site.register(m.Student)
admin.site.register(m.Department)
admin.site.register(m.Room)
admin.site.register(m.Major)
admin.site.register(m.Semester,SemesterAdmin)
admin.site.register(m.Specialization, SpecializationAdmin)
admin.site.register(m.Building)
admin.site.register(m.Professor)
admin.site.register(m.Course)
admin.site.register(m.Class)
admin.site.register(m.Announcement)
admin.site.register(m.AnnouncementText)
admin.site.register(m.SemesterCourseTuition)
admin.site.register(m.ClassAttendance)
admin.site.register(m.StudentClass)
admin.site.register(m.StudentInvoice)






