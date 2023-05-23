import requests
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PersonForm, FixedTuitionForm, StudentClassForm, ClassAttendanceForm, DepartmentForm, RoomForm, BuildingForm
from .models import Person, FixedTuitionFee, StudentClass, ClassAttendance, Department, Room, Building

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
    tuition = get_object_or_404(FixedTuitionFee, id = id )
    form = FixedTuitionForm(request.POST or None, instance=tuition)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "fixed_tuition_form.html", {"form":form})


def load_person_form(request, id):
    person = get_object_or_404(Person, national_id = id )
    form = PersonForm(request.POST or None, instance=person)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "person_form.html", {"form":form})


def home(request, student_id):
    
    BASE_URL = "http://127.0.0.1:8000/"
    current_term = request.GET.get("term")
    # student personal information
    req = requests.get(BASE_URL + f"edu/api/v1/panel/{student_id}?term={current_term}")
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
        }
        return render(request,'home.html', context=context)

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

def building_form(request):
    form = BuildingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "building_form.html", {"form":form})

def building_edit_form(request,id):
    building = get_object_or_404(Room, id = id )
    form = BuildingForm(request.POST or None, instance=building)
    if form.is_valid():
        form.save()
        return HttpResponse("SUCCESS")
    return render(request, "building_edit_form.html", {"form":form})

def login_form(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        BASE_URL = "http://127.0.0.1:8000/"
        # student personal information
        payload = {"username":username, "password":password}
        req = requests.post(BASE_URL + f"edu/api/token/",data=payload)
        if req.status_code == 200: 
            data = req.json()
            token = data["access"]
            request.session["jwt"]=token
            return redirect ("amuzeshyar:home", student_id=25)
        else:
            return HttpResponse("نام کاربری یا رمز عبور معتبر نمی باشد ")      
    return render(request, "login.html")