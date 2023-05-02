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

