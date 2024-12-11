from pickletools import uint1

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from resumebuilder.models import Experience, Skill, Job, Profile, PortfolioPiece
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from resumebuilder.forms import ExperienceForm, SkillForm, JobForm, PortfolioPieceForm

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

    keyskills = findKeySkills(currentuser)
    weakskills = findWeakSkills(currentuser)
    strongskills = findStrongSkills(currentuser)

    return render(request, "profile.html", {'profile': thisprofile, 'keyskills': keyskills, 'weakskills': weakskills, 'strongskills': strongskills})

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
def portfolio(request):
    currentuser = request.user
    thisprofile = Profile.objects.get(user=currentuser)
    pieces = thisprofile.portfoliopieces
    pieceform = PortfolioPieceForm(profile=thisprofile)
    return render(request, "portfolio.html", { 'pieces': pieces, 'pieceform': pieceform })

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
def addPiece(request):
    pieceform = PortfolioPieceForm(request.POST)

    if pieceform.is_valid():
        newpiece = pieceform.save()
        profile = Profile.objects.get(user=request.user)
        profile.portfoliopieces.add(PortfolioPiece.objects.get(pk=newpiece.pk))
    else:
        return HttpResponse("Invalid")
    return redirect(portfolio)

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
def deletePiece(request, id):
    PortfolioPiece.objects.get(pk=id).delete()
    return redirect(portfolio)

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
def editPiece(request, id):
    piece = PortfolioPiece.objects.get(pk=id)
    profile = Profile.objects.get(user=request.user)
    pieceform = PortfolioPieceForm(instance=piece, profile=profile)
    return render(request, "editpiece.html", { 'piece': piece, 'pieceform': pieceform })

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

@login_required(login_url='index')
def pieceEdit(request, id):
    piece = PortfolioPiece.objects.get(pk=id)
    pieceform = PortfolioPieceForm(request.POST)
    if pieceform.is_valid():
        piece.title = pieceform.cleaned_data['title']
        piece.description = pieceform.cleaned_data['description']
        piece.skills.set(pieceform.cleaned_data['skills'])
        piece.save()
        return redirect(portfolio)
    else:
        return HttpResponse("Invalid")

@login_required(login_url='index')
def buildResume(request, id):
    job = Job.objects.get(pk=id)

    experiences = []
    pieces = []
    for skill in job.skills.all():
        relevantexperience = Experience.objects.filter(skills=skill)
        relevantpiece = PortfolioPiece.objects.filter(skills=skill)

        for experience in relevantexperience:
            if experience not in experiences:
                experiences.append(experience)
        for piece in relevantpiece:
            if piece not in pieces:
                pieces.append(piece)
    experiences.sort(key=lambda experience: experience.startdate, reverse=True)

    sortpieces = []
    similarity = []
    for piece in pieces:
        count = 0
        for skill in piece.skills.all():
            if skill in job.skills.all():
                count += 1
        similarity.append(count)
    for piece in pieces:
        index = similarity.index(max(similarity))
        currpiece = pieces[index]
        sortpieces.append(currpiece)
        similarity[index] = -1


    return render(request, 'buildresume.html', { 'experiences': experiences, 'pieces': sortpieces })

def skillSortByJobAppearance(user):
    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    skills = profile.skills.all()
    priority = []
    priorityskills = []

    for skill in skills:
        count = sum(skill in job.skills.all() for job in jobs)
        priority.append(count)

    for skill in skills:
        index = priority.index(max(priority))
        if priority[index] == 0:
            return priorityskills
        else:
            priorityskills.append(skills[index])
        priority[index] = -1
    return priorityskills

def skillSortByExperienceAppearance(user):
    profile = Profile.objects.get(user=user)
    skills = profile.skills.all()
    experiences = profile.experiences.all()
    portfolio = profile.portfoliopieces.all()
    sortskill = []
    priority = []

    for skill in skills:
        inexperience = sum(skill in experience.skills.all() for experience in experiences) + sum(skill in piece.skills.all() for piece in portfolio)
        priority.append(inexperience)
    for skill in skills:
        index = priority.index(max(priority))
        sortskill.append(skills[index])
        priority[index] = -1
    return sortskill

def findKeySkills(user):
    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    skills = skillSortByJobAppearance(user)
    keyskills = []

    numkey = 3
    if numkey > len(skills):
        numkey = len(skills)

    for i in range(numkey):
        if sum(skills[i] in job.skills.all() for job in jobs) == 0:
            keyskills[i] = None
        else:
            keyskills.append(skills[i])

    return keyskills

def findWeakSkills(user):
    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    experiences = profile.experiences.all()
    portfolio = profile.portfoliopieces.all()
    skills = skillSortByJobAppearance(user)
    numweak = 3
    if numweak > len(skills):
        numweak = len(skills)
    weakskills = [None] * numweak
    priority = []

    for skill in skills:
        injobs = sum(skill in job.skills.all() for job in jobs)
        inexperience = sum(skill in experience.skills.all() for experience in experiences) + sum(skill in piece.skills.all() for piece in portfolio)
        priority.append(injobs - inexperience)
    for i in range(numweak):
        index = priority.index(min(priority))
        weakskills.append(skills[index])
        priority[index] = max(priority) + 1
    return weakskills


def findStrongSkills(user):
    skills = skillSortByExperienceAppearance(user)
    numstrong = 3
    if numstrong > len(skills):
        numstrong = len(skills)
    strongskills = [None] * numstrong

    for i in range(numstrong):
        strongskills[i] = skills[i]
    return strongskills