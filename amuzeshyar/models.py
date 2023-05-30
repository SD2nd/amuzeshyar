"""module docstring"""
from django.db import models
from django.contrib.auth.models import User


class CharFiledLength:
    short_title = 50
    long_title = 255
    description = 1000


class ConstValue(models.Model):
    title = models.CharField(max_length=CharFiledLength.long_title)
    parent = models.ForeignKey(
        to='ConstValue', on_delete=models.CASCADE, null=True, blank=True)

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

    def __str__(self) -> str:
        return f"{self.address} {self.person.__str__()}"


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

    def __str__(self) -> str:
        return f"{self.building.__str__()} {self.code}"


class Department(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    parent = models.ForeignKey(
        to="Department", on_delete=models.CASCADE, null=True, blank=True)
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

    def __str__(self) -> str:
        return self.person.__str__()


class Major(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    english_title = models.CharField(max_length=CharFiledLength.short_title)
    bachelor_unit = models.PositiveSmallIntegerField(
        verbose_name="تعداد واحد مورد نیاز برای کارشناسی", null=True)
    master_unit = models.PositiveSmallIntegerField(
        verbose_name="تعداد واحد مورد نیاز برای کارشناسی ارشد", null=True)
    phd_unit = models.PositiveSmallIntegerField(
        verbose_name="تعداد واحد مورد نیاز برای دکتری", null=True)

    def __str__(self):
        return self.title



class Semester(models.Model):
    class Meta:
        verbose_name = "نیمسال آموزشی"
        verbose_name_plural = "نیمسالهای آموزشی"

    semester_type = models.ForeignKey(
        ConstValue,
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="نوع نیمسال آموزشی")
    registration_start_date = models.DateField(verbose_name="تاریخ شروع ثبت نام")
    registration_end_date = models.DateField(verbose_name="تاریخ پایان ثبت نام")
    classes_start_date = models.DateField(verbose_name="تاریخ شروع کلاس")
    classes_end_date = models.DateField(verbose_name="تاریخ اتمام کلاس")
    registration_modification_start_date = models.DateField(
        null=True, blank=True,
        verbose_name="تاریخ شروع حذف و اضافه")
    registration_modification_end_date = models.DateField(
        null=True, blank=True,
        verbose_name="تاریخ اتمام حذف و اضافه")
    exams_start_date = models.DateField(verbose_name="تاریخ شروع امتحانات")
    exams_end_date = models.DateField(verbose_name="تاریخ اتمام امتحانات")
    year = models.PositiveSmallIntegerField(verbose_name="سال تحصیلی")

    def __str__(self):
        return f"{self.year} {self.semester_type.__str__()}"
    
    @property
    def semester_code(self):
        # hardcoded!
        term_type = {
            21:"1",
            22: "2" ,
            23: "3",
        }
        year_code = str(self.year)[2:]
        return year_code + term_type[self.semester_type.id]
        
        


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
    entry_year = models.SmallIntegerField(null=True)
    real_student_id = models.CharField(max_length=20, null=True, blank=True)
    auth_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.person.__str__()


class ProfessorEvaluationParameter(models.Model):
    title = models.CharField(max_length=CharFiledLength.long_title)
    evaluation_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title


class Specialization(models.Model):
    title = models.CharField(max_length=CharFiledLength.short_title)
    english_title = models.CharField(max_length=CharFiledLength.short_title)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    title = title = models.CharField(max_length=CharFiledLength.long_title, verbose_name="عنوان")
    english_title = models.CharField(max_length=CharFiledLength.long_title, verbose_name="عنوان لاتین")
    units_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_units_type", verbose_name="نوع واحد")
    theory_units = models.PositiveSmallIntegerField(default=0,  verbose_name="تعداد واحد نظری")
    practical_units = models.PositiveSmallIntegerField(default=0,  verbose_name="تعداد واحد عملی")
    course_type = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_course_type",  verbose_name="نوع درس")
    degree_level = models.ForeignKey(
        ConstValue, on_delete=models.SET_NULL, null=True, related_name="Course_degree_level",  verbose_name="مقطع تحصیلی")
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True,  verbose_name="گرایش درس")
    
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس ها"
        
    def __str__(self) -> str:
        return self.title

    @property
    def units(self):
        return self.practical_units + self.theory_units

class Class(models.Model):
    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاسها"

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,
        verbose_name = "درس")
    instructor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True,
        verbose_name = "استاد")
    capacity = models.PositiveSmallIntegerField(default=15,
        verbose_name = "ظرفیت کلاس")
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True,
        verbose_name = "نیمسال")
    exam_datetime = models.DateTimeField(verbose_name = "تاریخ امتحان")

    def __str__(self) -> str:
        return f"{self.course.__str__()} {self.instructor.__str__()} {self.semester.__str__()}"


class ProfessorEvaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(
        Professor, on_delete=models.SET_NULL, null=True)
    parameter = models.ForeignKey(
        ProfessorEvaluationParameter, on_delete=models.SET_NULL, null=True)
    point = models.PositiveSmallIntegerField(default=5)


class AnnouncementText(models.Model):
    description = models.CharField(max_length=CharFiledLength.description)
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.description


class Announcement(models.Model):
    announcement = models.ForeignKey(
        AnnouncementText,verbose_name="اطلاعیه", on_delete=models.SET_NULL, null=True)
    specific_major = models.ForeignKey(
        Major, verbose_name="رشته",on_delete=models.SET_NULL, null=True)
    specific_specialization = models.ForeignKey(
        Specialization,verbose_name="تخصص", on_delete=models.SET_NULL, null=True)
    specific_entry_semester = models.ForeignKey(
        Semester,verbose_name="نیمسال", on_delete=models.SET_NULL, null=True)
    specific_degree_level = models.ForeignKey(
        ConstValue,verbose_name="مقطع", on_delete=models.SET_NULL, null=True)
    specific_department = models.ForeignKey(
        Department,verbose_name="دپارتمان", on_delete=models.SET_NULL, null=True)
    specific_student = models.ForeignKey(
        Student,verbose_name="دانش آموز", on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(verbose_name="تاریخ انتشار",auto_now=True)
    expiration_datetime = models.DateTimeField(verbose_name="تاریخ انقضا", null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.specific_degree_level.parent.title.__str__()}"



class Email(models.Model):
    email = models.EmailField(max_length=CharFiledLength.long_title)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.email


class SemesterCourseTuition(models.Model):
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True)
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

    def __str__(self) -> str:
        return f"{self.student.__str__()} {self.session.__str__()} {self.grade}"


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

    def __str__(self) -> str:
        return f"{self.specialization.__str__()} {self.department.__str__()}"


class ClassSchedule(models.Model):
    class Meta:
        verbose_name = "زمانبندی کلاس"
        verbose_name_plural = "زمانهای کلاس"

    session = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True,
        verbose_name = "کلاس", related_name="class_schedule_children")
    day_of_week = models.PositiveSmallIntegerField(verbose_name = "روز هفته")
    start_at = models.TimeField(verbose_name = "زمان شروع")
    end_at = models.TimeField(verbose_name = "زمان پایان")
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True,
        verbose_name = "مکان")

    def __str__(self) -> str:
        return f"{self.session.__str__()} \
                 {self.day_of_week} \
                 {self.start_at} \
                 {self.end_at} \
                 {self.location.__str__()}"


class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.number


class FixedTuitionFee(models.Model):
    semester = models.ForeignKey(
        Semester, verbose_name="ترم", on_delete=models.SET_NULL, null=True)
    fee = models.IntegerField(verbose_name="مبلغ")
    year = models.PositiveSmallIntegerField(verbose_name="سال")
    field_of_study = models.ForeignKey(verbose_name="رشته تحصیلی",
                                       to="Major", on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return f"{self.semester.__str__()} {self.field_of_study.__str__()} {self.year}"

class StudentInvoice(models.Model):
    description = models.CharField(verbose_name="توضیحات",max_length=CharFiledLength.long_title)
    creation_date = models.DateField(verbose_name="تاریخ انتشار",)
    is_payed = models.BooleanField(verbose_name="وضعیت پرداخت", default=False)
    semester = models.ForeignKey(
        Semester, verbose_name="ترم", on_delete=models.SET_NULL, null=True)
    indebtedness = models.IntegerField(verbose_name="بدهی",)
    student = models.ForeignKey(Student,verbose_name="نام دانشجو", on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return f"{self.indebtedness}"


class StudentPayment(models.Model):
    datetime = models.DateTimeField(verbose_name="تاریخ", auto_now_add=True)
    semester = models.ForeignKey(Semester, verbose_name="ترم", on_delete=models.SET, null=True)
    amount = models.IntegerField(verbose_name="مبلغ",)
    payment_gateway = models.CharField(verbose_name="درگاه پرداخت", max_length=CharFiledLength.short_title)
    reference_code = models.CharField(
        verbose_name="کد ارجاع", max_length=CharFiledLength.long_title, null=True, blank=True)
    is_succeeded = models.BooleanField(verbose_name="وضعیت انجام تراکنش",default=True)
    invoice = models.ForeignKey(
        StudentInvoice, verbose_name="توضیحات صورتحساب", on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student,verbose_name="نام دانشجو", on_delete=models.SET_NULL, null=True)
    


class CoursePrerequisite(models.Model):
    c1 = models.ForeignKey(Course, on_delete=models.CASCADE,
                           related_name="CoursePrerequisite_c1",
                           verbose_name="درس1")
    is_prerequisite = models.BooleanField(default=False, verbose_name="پیشنیاز")
    is_concurrent = models.BooleanField(default=False, verbose_name="همنیاز")
    c2 = models.ForeignKey(Course, on_delete=models.CASCADE,
                           related_name="CoursePrerequisite_c2", 
                           verbose_name="درس2")
    
    class Meta:
        verbose_name = "نیازمندی  درس"
        verbose_name_plural = "نیازمندی های درس"
