from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from amuzeshyar import models as m


class PersonResponseSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = m.Person
        fields = "__all__"

    def get_role(self, obj):
        return obj.role.title if obj.role else None

    def get_gender(self, obj):
        return "مرد" if obj.gender else "زن"


class PersonRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Person
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Email
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PhoneNumber
        fields = "__all__"


class StudentResponseSerializer(serializers.ModelSerializer):
    person = PersonResponseSerializer()
    registration_type = serializers.SerializerMethodField()
    field_of_study = serializers.SerializerMethodField()
    graduation_date = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = m.Student
        fields = "__all__"
        extra_fields = ["email", "addresses", "phone_numbers"]

    def get_registration_type(self, obj):
        return obj.registration_type.title if obj.registration_type else None

    def get_field_of_study(self, obj):
        return obj.field_of_study.title if obj.field_of_study else None

    def get_graduation_date(self, obj):
        return obj.graduation_date if obj.graduation_date else "نامشخص"

    def get_addresses(self, obj):
        all_addresses = m.Address.objects.filter(person=obj.person)
        return [address.address for address in all_addresses]

    def get_emails(self, obj):
        all_emails = m.Email.objects.filter(person_id=obj.person_id)
        return [email.email for email in all_emails]

    def get_phone_numbers(self, obj):
        all_numbers = m.PhoneNumber.objects.filter(person_id=obj.person_id)
        return [phone.number for phone in all_numbers]


class StudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Student
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Address
        fields = "__all__"


class ClassAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ClassAttendance
        fields = "__all__"


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.StudentClass
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Course
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Room
        fields = "__all__"


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Building
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Department
        fields = "__all__"


class ConstValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ConstValue
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True, write_only=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user