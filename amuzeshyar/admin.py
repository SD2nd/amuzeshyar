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

admin.site.register(m.FixedTuitionFee, FixedTuitionAdmin)
admin.site.register(m.Person, PersonAdmin)
admin.site.register(m.Student)
admin.site.register(m.Department)
admin.site.register(m.Room)
