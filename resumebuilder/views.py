from http.client import HTTPResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from resumebuilder.models import Experience
from resumebuilder.forms import ExperienceForm


# Create your views here.
def index(request):
    experiences = Experience.objects.all()
    experienceform = ExperienceForm()
    return render(request, "index.html", { 'experiences': experiences, 'experienceform': experienceform })

def addExperience(request):
    experienceform = ExperienceForm(request.POST)

    if experienceform.is_valid():
        experienceform.save()
    else:
        return HTTPResponse("Invalid")

    return redirect(index)

def deleteExperience(request, id):
    Experience.objects.get(pk=id).delete()
    return redirect(index)
