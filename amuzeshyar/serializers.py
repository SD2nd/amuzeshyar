from rest_framework import serializers

from .models import (
    Person,
    Email,
    PhoneNumber,
    Student, 
    Address,
    )


class PersonSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = "__all__"

    def get_role(self, obj):
        return obj.role.title

    def get_gender(self, obj):
        if obj.gender:
            return "مرد"
        return "زن"
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class StudentResponseSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    registration_type = serializers.SerializerMethodField()
    field_of_study = serializers.SerializerMethodField()
    graduation_date = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    
    

    class Meta:
        model = Student
        fields = "__all__" 
        extra_fields = ["email","addresses", "phone_numbers"]
        

    def get_registration_type(self, obj):
        return obj.registration_type.title

    def get_field_of_study(self,obj):
        return obj.field_of_study.title

    
    def get_graduation_date(self,obj):
        if not obj.graduation_date:
            return "نا مشخص"
        return obj.graduation_date
    
    def get_addresses(self,obj):
        all_addresses=Address.objects.filter(person = obj.person)
        return [address.address for address in all_addresses]
    
    def get_emails(self, obj):
        all_emails = Email.objects.filter(person_id=obj.person_id)
        return [email.email for email in all_emails]
    
    
    def get_phone_numbers(self, obj):
        all_numbers = PhoneNumber.objects.filter(person_id=obj.person_id)
        return [phone.number for phone in all_numbers]
    
        
class StudentRequestSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    