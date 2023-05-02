from django import forms
from amuzeshyar import models as m


class PersonForm(forms.ModelForm):
    class Meta:
        model = m.Person
        fields = "__all__"