import datetime
from rest_framework import serializers

from amuzeshyar import models as m

class PersonResponseSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = m.Person
        fields = "__all__"

    def get_age(self, obj):
        
        return datetime.date.today().year - obj.birth_date.year
        
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
    passed_grades=serializers.SerializerMethodField()
    left_grades=serializers.SerializerMethodField()
    class Meta:
        model = m.Student
        fields = "__all__"
        extra_fields = ["email", "addresses", "phone_numbers"]

    
    def get_registration_type(self, obj):
        return obj.registration_type.title if obj.registration_type else None
    def get_passed_grades(self,obj):
        student_id =obj.id
        s =m.StudentClass.objects.filter(student_id=student_id, grade__gt = 10)
        return len(s)
    def get_left_grades(self,obj):
        student_id=obj.id
        units = obj.field_of_study.bachelor_unit
        passed=len(m.StudentClass.objects.filter(student_id=student_id, grade__gt = 10))
        
        return units-passed
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
        model= m.Department
        fields = "__all__"
class ConstValueSerializer(serializers.ModelSerializer):
    parent_title = serializers.SerializerMethodField()
    class Meta:
        model = m.ConstValue
        fields = "__all__"
    
    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else None
class FixedTuitionFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.FixedTuitionFee
        fields = "__all__"
class SemesterCourseTuitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SemesterCourseTuition
        fields = "__all__"
class StudentInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SemesterCourseTuition
        fields = "__all__"
class AnnouncementTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.AnnouncementText
        fields = "__all__"
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Announcement
        fields = "__all__"
    
    
