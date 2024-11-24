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

def editExperience(request, id):
    experience = Experience.objects.get(pk=id)
    experienceform = ExperienceForm(instance=experience)
    return render(request, "editexperience.html", { 'experience': experience, 'experienceform': experienceform })

def editSkill(request, id):
    skill = Skill.objects.get(pk=id)
    skillform = SkillForm(instance=skill)
    return render(request, "editskill.html", { 'skill': skill, 'skillform': skillform })

def experienceEdit(request, id):
    experience = Experience.objects.get(pk=id)
    experienceform = ExperienceForm(request.POST)
    if experienceform.is_valid():
        experience.title = experienceform.cleaned_data['title']
        experience.description = experienceform.cleaned_data['description']
        experience.startdate = experienceform.cleaned_data['startdate']
        experience.enddate = experienceform.cleaned_data['enddate']
        experience.current = experienceform.cleaned_data['current']
        experience.save()
        return redirect(experiences)
    else:
        return HttpResponse("Invalid")

def skillEdit(request, id):
    skill = Skill.objects.get(pk=id)
    skillform = SkillForm(request.POST)
    if skillform.is_valid():
        skill.title = skillform.cleaned_data['title']
        skill.save()
        return redirect(skills)
    else:
        return HttpResponse("Invalid")