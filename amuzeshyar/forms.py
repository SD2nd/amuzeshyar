from django import forms
from amuzeshyar import models as m


class PersonForm(forms.ModelForm):
    class Meta:
        model = m.Person
        fields = "__all__"


class FixedTuitionForm(forms.ModelForm):
    class Meta:
        model = m.FixedTuitionFee
        fields = "__all__"


class CourseTuitionForm(forms.ModelForm):
    class Meta:
        model = m.SemesterCourseTuition
        fields = "__all__"


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = m.StudentInvoice
        fields = "__all__"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = m.StudentPayment
        fields = "__all__"

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = m.Announcement
        fields = "__all__"

class SemesterForm(forms.ModelForm):
    class Meta:
        model = m.Semester
        fields = "__all__"
class ClassForm(forms.ModelForm):
    class Meta:
        model = m.Class
        fields = "__all__"
class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = m.ClassSchedule
        fields = "__all__"


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = m.Specialization
        fields = "__all__"

class StudentClassForm(forms.ModelForm):
    class Meta:
        model = m.StudentClass
        fields = "__all__"

class ClassAttendanceForm(forms.ModelForm):
    class Meta:
        model = m.ClassAttendance
        fields = "__all__"

class ClassAttendanceForm(forms.ModelForm):
    class Meta:
        model = m.ClassAttendance
        fields = "__all__"
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = m.Department
        fields = "__all__"

class RoomForm(forms.ModelForm):
    class Meta:
        model = m.Room
        fields = "__all__"

class BuildingForm(forms.ModelForm):
    class Meta:
        model = m.Building
        fields = "__all__"
