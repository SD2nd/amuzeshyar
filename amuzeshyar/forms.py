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

class SemesterForm(forms.ModelForm):
    class Meta:
        model = m.Semester
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
