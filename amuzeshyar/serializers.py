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

    student_str = serializers.SerializerMethodField()
    session_str = serializers.SerializerMethodField()
    class Meta:
        model = m.ClassAttendance
        fields = "__all__"
    def get_student_str(self, obj):
        return (obj.student.person.first_name + " " + obj.student.person.last_name)  if obj.student else None
    
    def get_session_str(self, obj):
        return obj.session.course.title  if obj.session else None

class StudentClassSerializer(serializers.ModelSerializer): 

    student_str = serializers.SerializerMethodField()
    session_str = serializers.SerializerMethodField()
    class Meta:
        model = m.StudentClass
        fields = "__all__"    

    def get_student_str(self, obj):
        return (obj.student.person.first_name + " " + obj.student.person.last_name)  if obj.student else None
    
    def get_session_str(self, obj):
        return obj.session.course.title  if obj.session else None

class CourseSerializer(serializers.ModelSerializer): 
    # course_type_title = serializers.SerializerMethodField()
    # degree_level_title = serializers.SerializerMethodField()
    # specialization = serializers.SerializerMethodField()
    
    class Meta:
        model = m.Course
        fields = "__all__" 
        # extra_fields = ["course_type_title","degree_level_title"] 
        #depth = 1
                
        # def get_course_type_title (self, obj):
        #      return obj.course_type.title
    
        # def get_degree_level_title (self, obj):
        #     return obj.degree_level.title
    
        # def get_specialization(self, obj):
        #  return obj.specialization.title
# 

class RoomSerializer(serializers.ModelSerializer):
    building_title = serializers.SerializerMethodField()
    room_title = serializers.SerializerMethodField()
    class Meta:
        model = m.Room
        fields = "__all__"

    def get_building_title (self, obj):
        return obj.building.title
    
    def get_room_title (self, obj):
        return obj.room_type.title
class BuildingSerializer(serializers.ModelSerializer):
    building_type_title = serializers.SerializerMethodField()
    class Meta: 
        model = m.Building
        fields = "__all__"

    
    def get_building_type_title (self, obj):
        return obj.building_type.title
    
    
    

    
class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= m.Department
        fields = "__all__"
        extra_fields = ["Department_title"]
    
class ConstValueSerializer(serializers.ModelSerializer):
    parent_title = serializers.SerializerMethodField()
    class Meta:
        model = m.ConstValue
        fields = "__all__"
    
    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else None


class FixedTuitionFeeSerializer(serializers.ModelSerializer):
    field_of_study_str = serializers.SerializerMethodField()
    semester_str = serializers.SerializerMethodField()

    class Meta:
        model = m.FixedTuitionFee
        fields = "__all__"

    def get_field_of_study_str(self, obj):
        return  obj.field_of_study.title if obj.field_of_study else None
    def get_semester_str(self, obj):
        return  obj.semester.registration_start_date if obj.semester else None

class SemesterCourseTuitionSerializer(serializers.ModelSerializer):
    course_type_str = serializers.SerializerMethodField()
    field_of_study_str = serializers.SerializerMethodField()
    unit_type_str = serializers.SerializerMethodField()

    class Meta:
        model = m.SemesterCourseTuition
        fields = "__all__"

    def get_course_type_str(self, obj):
        return obj.course_type.title if obj.course_type else None
    def get_field_of_study_str(self, obj):
        return  obj.field_of_study.title if obj.field_of_study else None
    def get_unit_type_str(self, obj):
        return  obj.unit_type.title if obj.unit_type else None


class StudentInvoiceSerializer(serializers.ModelSerializer):
    semester_str = serializers.SerializerMethodField()
    student_str = serializers.SerializerMethodField()

    class Meta:
        model = m.StudentInvoice
        fields = "__all__"

    def get_semester_str(self, obj):
        return obj.semester.registration_start_date if obj.semester else None
    def get_student_str(self, obj):
        return (obj.student.person.first_name + " " + obj.student.person.last_name)  if obj.student else None


class StudentPaymentSerializer(serializers.ModelSerializer):
    semester_str = serializers.SerializerMethodField()
    student_str = serializers.SerializerMethodField()
    invoice_str = serializers.SerializerMethodField()

    class Meta:
        model = m.StudentPayment
        fields = "__all__"

    def get_semester_str(self, obj):
        return obj.semester.registration_start_date if obj.semester else None
    def get_student_str(self, obj):
        return (obj.student.person.first_name + " " + obj.student.person.last_name) if obj.student else None
    def get_invoice_str(self, obj):
        return obj.invoice.description if obj.invoice else None


class AnnouncementTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.AnnouncementText
        fields = "__all__"

class AnnouncementSerializer(serializers.ModelSerializer):
    specific_major_str = serializers.SerializerMethodField()
    specific_specialization_str = serializers.SerializerMethodField()
    specific_entry_semester_str = serializers.SerializerMethodField()
    specific_degree_level_str = serializers.SerializerMethodField()
    specific_department_str = serializers.SerializerMethodField()
    specific_student_str = serializers.SerializerMethodField()
    class Meta:
        model = m.Announcement
        fields = "__all__"
    def get_specific_major_str(self, obj):
        return obj.specific_major.title if obj.specific_major else None
    def get_specific_specialization_str(self, obj):
        return obj.specific_specialization.title if obj.specific_specialization else None
    def get_specific_entry_semester_str(self, obj):
        return obj.specific_entry_semester.registration_start_date if obj.specific_entry_semester else None
    def get_specific_degree_level_str(self, obj):
        return obj.specific_degree_level.title if obj.specific_degree_level else None
    def get_specific_department_str(self, obj):
        return obj.specific_department.title if obj.specific_department else None
    def get_specific_student_str(self, obj):
        return (obj.specific_student.person.first_name + " " + obj.specific_student.person.last_name) if obj.specific_student else None

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Semester
        fields = "__all__"
        
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Class
        fields = "__all__"
        
class ClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ClassSchedule
        fields = "__all__"

class SpecializationSerializer(serializers.ModelSerializer):
   major_title = serializers.SerializerMethodField()
   class Meta:
       model = m.Specialization
       fields = "__all__"
   def get_major_title(self, obj):
       return obj.major.title
class FirstPageInformationSerializer(serializers.Serializer):
    # basic information 
    firstname = serializers.CharField(source="person.first_name")
    lastname = serializers.CharField(source="person.last_name")
    field_of_study = serializers.CharField()
    gender = serializers.BooleanField(source="person.gender")

    # units, GPA information 
    units_passed = serializers.SerializerMethodField()
    units_taken = serializers.SerializerMethodField()
    total_units = serializers.SerializerMethodField()
    gpa = serializers.SerializerMethodField(method_name="calc_gpa")
    
    # financial information
    current_term_payed_fee = serializers.SerializerMethodField(method_name="calc_current_term_payed_fee")
    all_term_payed_fee = serializers.SerializerMethodField(method_name="calc_all_term_payed_fee")
    all_must_be_paid = serializers.SerializerMethodField(method_name="calc_all_must_be_paid")
    
    # class scheduling information
    classes_schedule = serializers.SerializerMethodField()
    
    def get_units_passed(self, obj):
        units = 0
        passed_units_qs = m.StudentClass.objects.filter(grade__gte=10).filter(student_id = obj.id)
        if not passed_units_qs.exists():
            raise Exception("There is no StudentClass record")
        for record in passed_units_qs:
            units += record.session.course.practical_units + \
                     record.session.course.theory_units 
        return units

    def get_units_taken(self, obj):
        units = 0
        passed_units_qs = m.StudentClass.objects.filter(student_id = obj.id)
        if not passed_units_qs.exists():
            raise Exception("There is no StudentClass record")
        for record in passed_units_qs:
            units += record.session.course.practical_units + \
                     record.session.course.theory_units 
        return units
    
    def get_total_units(self, obj):
        total_units = obj.field_of_study.bachelor_unit
        return total_units 
    
    def calc_gpa(self, obj):
        units = 0
        weighted_sum = 0
        passed_units_qs = m.StudentClass.objects.filter(grade__gte=10).filter(student_id = obj.id)
        if not passed_units_qs.exists():
            raise Exception("There is no StudentClass record")
        for record in passed_units_qs:
            this_units = record.session.course.practical_units + \
                         record.session.course.theory_units 
            units += this_units
            weighted_sum += record.grade * this_units
        
        return round(weighted_sum / units, 2)
       
        
    def calc_current_term_payed_fee(self, obj):
        current_term = self.context.get("current_term")
        student_all_pays = m.StudentPayment.objects.filter(student_id = obj.id)
        if not student_all_pays.exists():
            return "No payment record found for student"
        current_term_student_payments = []
        for record in student_all_pays:
            if record.semester.semester_code == current_term:
                current_term_student_payments.append(record)
        current_term_student_payed_amount = 0       
        for record in current_term_student_payments:
            current_term_student_payed_amount += record.amount
        return current_term_student_payed_amount
    
    def calc_all_term_payed_fee(self, obj):
        student_all_pays = m.StudentPayment.objects.filter(student_id = obj.id)
        if not student_all_pays.exists():
            return "No payment record found for student"
        all_term_student_payed_amount = 0       
        for record in student_all_pays:
            all_term_student_payed_amount += record.amount
        return all_term_student_payed_amount
    
    def calc_all_must_be_paid(self, obj):
        # fixed term amount
        qs = m.Class.objects.values("semester").distinct()
        if not qs.exists():
            raise ValueError("There is no class record for student ")
        student_fixed_fee = m.FixedTuitionFee.objects.filter(year = obj.entry_year).first()
        if not student_fixed_fee:
            raise Exception(" There is no FixedTuitionFee record to fetch for this entry year")
        student_terms = len(qs)
        total_fixed_fee = student_terms*student_fixed_fee.fee
        
        # course fees
        taken_courses_qs = m.StudentClass.objects.filter(student_id=obj.id) 
        if not taken_courses_qs.exists():
            raise Exception("There is no StudentClass record to fetch for this")
        
        course_fees = 0
        for record in taken_courses_qs:
            try:
                fee_per_unit = m.SemesterCourseTuition.objects \
                .filter(course_type = record.session.course.course_type) \
                .filter(unit_type = record.session.course.units_type) \
                .filter(semester_id=record.session.semester_id)\
                .first().tuition_per_unit 
            except AttributeError:
                raise Exception("THERE IS NO SemesterCourseTuition VALID FOR THE SELECTED COURSE")
            course_fees += record.session.course.units * fee_per_unit 
        
        # calc debt
        return course_fees + total_fixed_fee
    
    def get_classes_schedule(self, obj):
        current_term = self.context.get("current_term")
        semesters_qs = m.Semester.objects.all()
        if not semesters_qs.exists():
            raise Exception("There is no Semester record!!!!!!")
        term_id = None
        # getting current term_id
        for record in semesters_qs:
            if record.semester_code == current_term:
                term_id = record.id
        
        classes_qs = m.StudentClass.objects.filter(student_id = obj.id, session__semester_id= term_id)
        if not classes_qs.exists():
            raise Exception("There is no No class record for this student in this Semester!")
        
        day_of_week = {
            1: "Saturday", 
            2: "Sunday",
            3: "Monday",
            4: "Tuesday",
            5: "Wednesday",
            6: "Thursday",
            7: "Friday",
        }
        schedules = []
        counter = 0
        for record in classes_qs:
            counter += 1
            class_sc =record.session.class_schedule_children.first() 
            class_time = f"{class_sc.start_at}-{class_sc.end_at} {day_of_week[class_sc.day_of_week]}"
            class_schedule = {
                "row": counter,
                "class_name": record.session.course.title,
                "instructor": record.session.instructor.__str__(),
                "time": class_time,
                "exam_date": record.session.exam_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "location": record.session.class_schedule_children.first().location_id
            }
            schedules.append(class_schedule)
        return schedules

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try: 
            rep["remaining_units"] = rep["total_units"] - rep["units_passed"]
        except Exception as e:
            rep["remaining_units"] = "Error!"
        rep["fullname"] = rep["firstname"] + " " + rep["lastname"]
        rep["debt"] = rep["all_must_be_paid"] - rep["all_term_payed_fee"]
        return rep
        
    
    