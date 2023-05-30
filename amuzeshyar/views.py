import requests
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import CourseForm, PersonForm, FixedTuitionForm, StudentClassForm, ClassAttendanceForm, DepartmentForm, RoomForm,SemesterForm,ClassForm,ClassScheduleForm, BuildingForm,AnnouncementForm, CourseTuitionForm, PaymentForm, InvoiceForm
from .models import Course,Person, FixedTuitionFee, StudentClass, ClassAttendance, Department, Room,Semester,Class,ClassSchedule, Building, Student, SemesterCourseTuition, StudentPayment, StudentInvoice

# Create your views here.

def person_form(request):
    form = PersonForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "person_form.html", {"form":form})
def fixed_tuition_form(request):
    form = FixedTuitionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "fixed_tuition_form.html", {"form":form})

def fixed_tuition_edit_form(request,id):
    tuition = get_object_or_404(FixedTuitionFee, id=id)
    form = FixedTuitionForm(request.POST or None, instance=tuition)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "fixed_tuition_form.html", {"form":form})

def course_tuition_form(request):
    form = CourseTuitionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "course_tuition_form.html", {"form":form})

def course_tuition_edit_form(request,id):
    tuition = get_object_or_404(SemesterCourseTuition, id=id)
    form = CourseTuitionForm(request.POST or None, instance=tuition)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "course_tuition_form.html", {"form":form})

def invoice_form(request):
    form = InvoiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "invoice_form.html", {"form":form})

def invoice_edit_form(request,id):
    invoice = get_object_or_404(StudentInvoice, id=id)
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "invoice_form.html", {"form":form})

def payment_form(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "payment_form.html", {"form":form})

def payment_edit_form(request,id):
    payment = get_object_or_404(StudentPayment, id=id)
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "payment_form.html", {"form":form})

def announcement_form(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "announcement_form.html", {"form":form})

def announcement_edit_form(request,id):
    ann = get_object_or_404(AnnouncementForm, id = id )
    form = AnnouncementForm(request.POST or None, instance=ann)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "announcement_form.html", {"form":form})



def load_person_form(request, id):
    person = get_object_or_404(Person, national_id = id )
    form = PersonForm(request.POST or None, instance=person)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "person_form.html", {"form":form})


def home(request, student_id):
    
    BASE_URL = "http://127.0.0.1:8000/"
    current_term = request.GET.get("term") or "012"
    # student personal information
    req = requests.get(
        BASE_URL + f"edu/api/v1/panel/{student_id}?term={current_term}",
        headers={
            "Authorization":"Bearer " + request.session.get("jwt") or None,
        }
        )
    if req.status_code == 200: 
        data = req.json()
        context = {
            "fullname": data["fullname"],
            "major": data["field_of_study"],
            "units_passed": data["units_passed"],
            "units_taken": data["units_taken"],
            "remaining_units": data["remaining_units"],
            "gpa": data["gpa"],
            "current_term_payed_fee": data["current_term_payed_fee"],
            "all_term_payed_fee": data["all_term_payed_fee"],
            "all_must_be_paid":data["all_must_be_paid"],
            "debt":data["debt"],
            "classes_schedule":data["classes_schedule"],
        }
        return render(request,'home.html', context=context)
    else: 
        return HttpResponse(f"{req.text}")

def student_class_form(request):
    form = StudentClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "student_class_form.html", {"form":form})


def student_class_edit_form(request,id):
    studentClass = get_object_or_404(StudentClass, id = id )
    form = StudentClassForm(request.POST or None, instance=studentClass)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "student_class_edit_form.html", {"form":form})

def class_attendance_form(request):
    form = ClassAttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "class_attendance_form.html", {"form":form})


def class_attendance_edit_form(request,id):
    classAttendance = get_object_or_404(ClassAttendance, id = id )
    form = ClassAttendanceForm(request.POST or None, instance=classAttendance)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "class_attendance_form.html", {"form":form})
        
        
    # units information
        
def department_form(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "department_form.html", {"form":form})

def department_edit_form(request,id):
    department = get_object_or_404(Department, id = id )
    form = DepartmentForm(request.POST or None, instance=Department)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "departmnet_edit_form.html", {"form":form})

def course_form(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "course_form.html", {"form":form})

def course_edit_form(request,id):
    course = get_object_or_404(Course, id = id )
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "course_form.html", {"form":form})

def room_form(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "room_form.html", {"form":form})

def room_edit_form(request,id):
    room = get_object_or_404(Room, id = id )
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "room_edit_form.html", {"form":form})

def semester_form(request):
    form = SemesterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "semester_form.html", {"form":form})

def semester_edit_form(request,id):
    room = get_object_or_404(Semester, id = id )
    form = SemesterForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "semester_form.html", {"form":form})
def class_form(request):
    form = ClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "class_form.html", {"form":form})

def class_edit_form(request,id):
    room = get_object_or_404(Class, id = id )
    form = ClassForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "class_form.html", {"form":form})

def classSchedule_form(request):
    form = ClassScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "classSch_form.html", {"form":form})

def classSchedule_edit_form(request,id):
    classSch = get_object_or_404(ClassSchedule, id = id )
    form = ClassScheduleForm(request.POST or None, instance=classSch)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "classSch_form.html", {"form":form})

def building_form(request):
    form = BuildingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "building_form.html", {"form":form})

def building_edit_form(request,id):
    building = get_object_or_404(Building, id = id )
    form = BuildingForm(request.POST or None, instance=building)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "building_edit_form.html", {"form":form})

def login_form(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")
        
        student = Student.objects.filter(real_student_id=student_id).first()
        
        if not student or not student.auth_user: 
            return HttpResponse("ERROR- STUDENT NOT FOUND", status=404)
        username = student.auth_user.username
        
        
        # calling API
        # student personal information
        BASE_URL = "http://127.0.0.1:8000/"
        payload = {
            "username":username,
            "password":password
            }
        req = requests.post(BASE_URL + f"edu/api/token/",data=payload)
        if req.status_code == 200: 
            data = req.json()
            token = data["access"]
            request.session["jwt"]=token
            return redirect ("amuzeshyar:home", student_id=student.id)
        elif req.status_code == 403:
            return HttpResponse("Token is invalid")    
        elif req.status_code == 401:
            return HttpResponse("Password is invalid")    

              
    return render(request, "login.html")