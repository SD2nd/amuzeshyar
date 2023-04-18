from rest_framework import serializers
from .models import Person, Email, PhoneNumber
# create your serializers here
# https://www.django-rest-framework.org/tutorial/quickstart/

class PersonSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'national_id', 'father_name', 'role', 'gender','birth_date')

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"
        

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"