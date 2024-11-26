from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from resumebuilder.models import Experience, Skill, Job
from resumebuilder.forms import ExperienceForm, SkillForm, JobForm


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

def jobs(request):
    jobs = Job.objects.all()
    jobform = JobForm()
    return render(request, "jobs.html", { 'jobs': jobs, 'jobform': jobform })

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

def addJob(request):
    jobform = JobForm(request.POST)

    if jobform.is_valid():
        jobform.save()
    else:
        return HttpResponse("Invalid")

    return redirect(jobs)

def deleteExperience(request, id):
    Experience.objects.get(pk=id).delete()
    return redirect(experiences)

def deleteSkill(request, id):
    Skill.objects.get(pk=id).delete()
    return redirect(skills)

def deleteJob(request, id):
    Job.objects.get(pk=id).delete()
    return redirect(jobs)

def editExperience(request, id):
    experience = Experience.objects.get(pk=id)
    experienceform = ExperienceForm(instance=experience)
    return render(request, "editexperience.html", { 'experience': experience, 'experienceform': experienceform })

def editSkill(request, id):
    skill = Skill.objects.get(pk=id)
    skillform = SkillForm(instance=skill)
    return render(request, "editskill.html", { 'skill': skill, 'skillform': skillform })

def editJob(request, id):
    job = Job.objects.get(pk=id)
    jobform = JobForm(instance=job)
    return render(request, "editjob.html", { 'job': job, 'jobform': jobform })

def experienceEdit(request, id):
    experience = Experience.objects.get(pk=id)
    experienceform = ExperienceForm(request.POST)
    if experienceform.is_valid():
        experience.title = experienceform.cleaned_data['title']
        experience.description = experienceform.cleaned_data['description']
        experience.startdate = experienceform.cleaned_data['startdate']
        experience.enddate = experienceform.cleaned_data['enddate']
        experience.current = experienceform.cleaned_data['current']
        experience.skills.set(experienceform.cleaned_data['skills'])
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

def jobEdit(request, id):
    job = Job.objects.get(pk=id)
    jobform = JobForm(request.POST)
    if jobform.is_valid():
        job.title = jobform.cleaned_data['title']
        job.link = jobform.cleaned_data['link']
        job.notes = jobform.cleaned_data['notes']
        job.skills.set(jobform.cleaned_data['skills'])
        job.save()
        return redirect(jobs)
    else:
        return HttpResponse("Invalid")