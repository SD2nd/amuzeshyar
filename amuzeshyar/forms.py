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