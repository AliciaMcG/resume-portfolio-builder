from pickletools import uint1

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from resumebuilder.models import Experience, Skill, Job, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from resumebuilder.forms import ExperienceForm, SkillForm, JobForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('profile')
    signupform = UserCreationForm()
    return render(request, "index.html", {'signupform':signupform})

def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username).exists():
        return HttpResponse("User does not exist")
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse("Invalid password")
    login(request, user)
    return redirect('profile')

def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if User.objects.filter(username=username).exists():
        return HttpResponse("Username is taken")
    user = User.objects.create_user(username=username)
    user.set_password(password)
    user.save()
    profile = Profile(user=user)
    profile.save()
    login(request, user)

    return redirect('index')

def signout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='index')
def profile(request):
    currentuser = request.user
    if not hasattr(currentuser, 'profile'):
        Profile.objects.create(user=currentuser)
    thisprofile = Profile.objects.get(user=currentuser)
    return render(request, "profile.html", {'profile': thisprofile})

@login_required(login_url='index')
def experiences(request):
    currentuser = request.user
    if not hasattr(currentuser, 'profile'):
        Profile.objects.create(user=currentuser)
    thisprofile = Profile.objects.get(user=currentuser)
    experiences = thisprofile.experiences
    experienceform = ExperienceForm(profile=thisprofile)
    return render(request, "experiences.html", { 'experiences': experiences, 'experienceform': experienceform })

@login_required(login_url='index')
def skills(request):
    currentuser = request.user
    thisprofile = Profile.objects.get(user=currentuser)
    skills = thisprofile.skills
    skillform = SkillForm()
    return render(request, "skills.html", { 'skills': skills, 'skillform': skillform })

@login_required(login_url='index')
def jobs(request):
    currentuser = request.user
    thisprofile = Profile.objects.get(user=currentuser)
    jobs = thisprofile.jobs
    jobform = JobForm(profile=thisprofile)
    return render(request, "jobs.html", { 'jobs': jobs, 'jobform': jobform })

@login_required(login_url='index')
def addExperience(request):
    experienceform = ExperienceForm(request.POST)

    if experienceform.is_valid():
        newexperience = experienceform.save()
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.experiences.add(Experience.objects.get(pk=newexperience.pk))
    else:
        return HttpResponse("Invalid")

    return redirect(experiences)

@login_required(login_url='index')
def addSkill(request):
    skillform = SkillForm(request.POST)

    if skillform.is_valid():
        if not Skill.objects.filter(title=skillform.cleaned_data['title']).exists():
            skillform.save()
        currentuser = request.user
        thisprofile = Profile.objects.get(user=currentuser)
        thisprofile.skills.add(Skill.objects.get(title=skillform.cleaned_data['title']))
    else:
        return HttpResponse("Invalid")

    return redirect(skills)

@login_required(login_url='index')
def addJob(request):
    jobform = JobForm(request.POST)

    if jobform.is_valid():
        newjob = jobform.save()
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.jobs.add(Job.objects.get(pk=newjob.pk))
    else:
        return HttpResponse("Invalid")

    return redirect(jobs)

@login_required(login_url='index')
def deleteExperience(request, id):
    Experience.objects.get(pk=id).delete()
    return redirect(experiences)

@login_required(login_url='index')
def deleteSkill(request, id):
    currentuser = request.user
    thisprofile = Profile.objects.get(user=currentuser)
    thisprofile.skills.remove(Skill.objects.get(pk=id))

    currentskill = Skill.objects.get(pk=id)
    profilecount = currentskill.profile.all().count()
    if profilecount == 0:
        Skill.objects.get(pk=id).delete()
    return redirect(skills)

@login_required(login_url='index')
def deleteJob(request, id):
    Job.objects.get(pk=id).delete()
    return redirect(jobs)

@login_required(login_url='index')
def editExperience(request, id):
    experience = Experience.objects.get(pk=id)
    profile = Profile.objects.get(user=request.user)
    experienceform = ExperienceForm(instance=experience, profile=profile)
    return render(request, "editexperience.html", { 'experience': experience, 'experienceform': experienceform })

@login_required(login_url='index')
def editSkill(request, id):
    skill = Skill.objects.get(pk=id)
    skillform = SkillForm(instance=skill)
    return render(request, "editskill.html", { 'skill': skill, 'skillform': skillform })

@login_required(login_url='index')
def editJob(request, id):
    job = Job.objects.get(pk=id)
    profile = Profile.objects.get(user=request.user)
    jobform = JobForm(instance=job, profile=profile)
    return render(request, "editjob.html", { 'job': job, 'jobform': jobform })

@login_required(login_url='index')
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

@login_required(login_url='index')
def skillEdit(request, id):
    skill = Skill.objects.get(pk=id)
    skillform = SkillForm(request.POST)

    if skillform.is_valid():
        # if only instance of skill, edit the instance
        profilecount = skill.profile.all().count()
        if profilecount == 1:
            if skillform.is_valid():
                skill.title = skillform.cleaned_data['title']
                skill.save()
                return redirect(skills)
        # if not only instance, remove from user's skills
        currentuser = request.user
        thisprofile = Profile.objects.get(user=currentuser)
        thisprofile.skills.remove(Skill.objects.get(pk=id))

        # if skill from skillform exists, add to user skills
        if Skill.objects.filter(title=skillform.cleaned_data['title']).exists():
            thisprofile.skills.add(Skill.objects.get(title=skillform.cleaned_data['title']))
            thisprofile.save()
            return redirect(skills)

        # if skill does not exist, create new skill
        newskill = Skill(title=skillform.cleaned_data['title'])
        thisprofile.skills.add(newskill)
        thisprofile.save()

    return HttpResponse("Invalid")

@login_required(login_url='index')
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