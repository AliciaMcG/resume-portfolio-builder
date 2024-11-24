from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from resumebuilder.models import Experience, Skill
from resumebuilder.forms import ExperienceForm, SkillForm


# Create your views here.
def index(request):
    return render(request, "index.html")

def experiences(request):
    experiences = Experience.objects.all()
    experienceform = ExperienceForm()
    return render(request, "experiences.html", { 'experiences': experiences, 'experienceform': experienceform })

def skills(request):
    skills = Skill.objects.all()
    skillform = SkillForm()
    return render(request, "skills.html", { 'skills': skills, 'skillform': skillform })

def addExperience(request):
    experienceform = ExperienceForm(request.POST)

    if experienceform.is_valid():
        experienceform.save()
    else:
        return HttpResponse("Invalid")

    return redirect(experiences)

def addSkill(request):
    skillform = SkillForm(request.POST)

    if skillform.is_valid():
        skillform.save()
    else:
        return HttpResponse("Invalid")

    return redirect(skills)

def deleteExperience(request, id):
    Experience.objects.get(pk=id).delete()
    return redirect(experiences)

def deleteSkill(request, id):
    Skill.objects.get(pk=id).delete()
    return redirect(skills)
