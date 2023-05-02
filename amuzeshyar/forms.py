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