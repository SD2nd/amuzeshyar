"""module docstring"""
from django.db import models


class CharFiledLength:
    short_title = 50
    long_title = 255
    description = 1000


class ConstValue(models.Model):
    title = models.CharField(max_length=CharFiledLength.long_title)
    parent = models.ForeignKey(to='ConstValue', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Person(models.Model):
    first_name = models.CharField(
        verbose_name="نام",
        max_length=CharFiledLength.short_title)
    last_name = models.CharField(
        verbose_name="نام خانوادگی",
        max_length=CharFiledLength.short_title)
    national_id = models.CharField(
        verbose_name="کدملی",
        max_length=10,
        db_column="national_id",
        primary_key=True,
        db_index=True
    )
    father_name = models.CharField(
        verbose_name="نام بدر", max_length=CharFiledLength.short_title)
    role = models.ForeignKey(
        ConstValue, verbose_name="نقش سازمانی", on_delete=models.SET_NULL, null=True)
    gender = models.BooleanField(verbose_name="جنسیت", default=0)
    birth_date = models.DateField(verbose_name=" تاریخ تولد", )

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Address(models.Model):
    address = models.CharField(max_length=CharFiledLength.description)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=True)


class Building(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    building_type = models.ForeignKey(
        ConstValue,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return self.title


class Room(models.Model):
    code = models.CharField(max_length=10, db_column="code", primary_key=True)
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True)
    floor = models.SmallIntegerField()
    block = models.CharField(max_length=1, null=True, blank=True)
    title = models.CharField(max_length=CharFiledLength.short_title)
    capacity = models.PositiveSmallIntegerField()
    room_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)


class Department(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    parent = models.ForeignKey(to="Department", on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title


class Professor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    academic_rank = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Professor_academic_rank")
    contract_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Professor_contract_type")
    faculty_member = models.BooleanField(default=False)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    research_area = models.CharField(max_length=CharFiledLength.long_title)


class Major(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    english_title = models.CharField(max_length=CharFiledLength.short_title)
    def __str__(self):
        return self.title


class Semester(models.Model):
    semester_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    classes_start_date = models.DateField()
    classes_end_date = models.DateField()
    registration_modification_start_date = models.DateField(
        null=True, blank=True)
    registration_modification_end_date = models.DateField(
        null=True, blank=True)
    exams_start_date = models.DateField()
    exams_end_date = models.DateField()
    year = models.PositiveSmallIntegerField()
    def __str__(self):
        return str(self.year)


class Student(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    registration_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)
    entry_date = models.DateField()
    entry_semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
    field_of_study = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True)
    graduation_date = models.DateField(null=True, blank=True)


class ProfessorEvaluationParameter(models.Model):
    title = models.CharField(max_length=CharFiledLength.long_title)
    evaluation_type = models.ForeignKey(ConstValue, on_delete=models.SET_NULL, null=True)


class Specialization(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    english_title = models.CharField(max_length=CharFiledLength.short_title)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)


class Course(models.Model):
    title = title = models.CharField(max_length=CharFiledLength.long_title)
    english_title = models.CharField(max_length=CharFiledLength.long_title)
    units_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_units_type")
    theory_units = models.PositiveSmallIntegerField(default=0)
    practical_units = models.PositiveSmallIntegerField(default=0)
    course_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_course_type")
    degree_level = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_degree_level")
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True)


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveSmallIntegerField(default=15)
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
    exam_datetime = models.DateTimeField()


class ProfessorEvaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True)
    parameter = models.ForeignKey(
        ProfessorEvaluationParameter, on_delete=models.SET_NULL, null=True)
    point = models.PositiveSmallIntegerField(default=5)


class AnnouncementText(models.Model):
    description = models.CharField(max_length=CharFiledLength.description)
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)


class Announcement(models.Model):
    announcement = models.ForeignKey(
        AnnouncementText, on_delete=models.SET_NULL, null=True)
    specific_major = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True)
    specific_specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True)
    specific_entry_semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
    specific_degree_level = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)
    specific_department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    specific_student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField(null=True, blank=True)


class Email(models.Model):
    email = models.EmailField(max_length=CharFiledLength.long_title)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)


class SemesterCourseTuition(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    field_of_study = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True)
    course_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="SemesterCourseTuition_course_type")
    unit_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="SemesterCourseTuition_unit_type")
    tuition_per_unit = models.IntegerField()


class ClassAttendance(models.Model):
    session_number = models.PositiveSmallIntegerField()
    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)


class StudentClass(models.Model):
    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    after_appeal_grade = models.PositiveSmallIntegerField(
        null=True, blank=True)
    is_active = models.BooleanField(default=True)


class GradeAppeal(models.Model):
    appeal_description = models.CharField(
        max_length=CharFiledLength.description)
    status = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)
    reply_description = models.CharField(
        max_length=CharFiledLength.description)
    submission_datetime = models.DateTimeField(auto_now=True)
    reply_datetime = models.DateTimeField(null=True, blank=True)
    class_student = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, null=True)


class MajorSpecializationDepartment(models.Model):
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)


class ClassSchedule(models.Model):
    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    day_of_week = models.PositiveSmallIntegerField()
    start_at = models.TimeField()
    end_at = models.TimeField()
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)


class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class FixedTuitionFee(models.Model):
    semester = models.ForeignKey(Semester,verbose_name="ترم", on_delete=models.SET_NULL, null=True)
    fee = models.IntegerField(verbose_name="مبلغ")
    year = models.PositiveSmallIntegerField(verbose_name="سال")
    field_of_study = models.ForeignKey(verbose_name="رشته تحصیلی",
                                       to="Major", on_delete=models.SET_NULL, null=True)


class StudentInvoice(models.Model):
    description = models.CharField(max_length=CharFiledLength.long_title)
    creation_date = models.DateField()
    is_payed = models.BooleanField(default=False)
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
    indebtedness = models.IntegerField()


class StudentPayment(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET, null=True)
    amount = models.IntegerField()
    payment_gateway = models.CharField(max_length=CharFiledLength.short_title)
    reference_code = models.CharField(
        max_length=CharFiledLength.long_title, null=True, blank=True)
    is_succeeded = models.BooleanField(default=True)
    invoice = models.ForeignKey(
        StudentInvoice, on_delete=models.SET_NULL, null=True)


class CoursePrerequisite(models.Model):
    c1 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="CoursePrerequisite_c1")
    is_prerequisite = models.BooleanField(default=False)
    is_concurrent = models.BooleanField(default=False)
    c2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="CoursePrerequisite_c2")
