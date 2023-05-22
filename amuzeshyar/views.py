import requests
from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import PersonForm, FixedTuitionForm
from .models import Person, FixedTuitionFee

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
        
        
    # units information
        
    return render(request,'home.html', context=context)

