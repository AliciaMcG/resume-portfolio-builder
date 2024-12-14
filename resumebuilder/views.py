from pickletools import uint1
from django.http import HttpResponse
import os
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
    if request.user.is_authenticated: #signed in users don't need to sign in again
        return redirect('profile')
    signupform = UserCreationForm()
    return render(request, "index.html", {'signupform':signupform})

def signin(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username).exists(): #make sure user exists
        return HttpResponse("User does not exist.")

    user = authenticate(username=username, password=password)
    if user is None: #make sure user entered right password
        return HttpResponse("Invalid password.")
    login(request, user)

    return redirect('profile')

def signup(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    username = request.POST.get('username')
    password = request.POST.get('password')
    if User.objects.filter(username=username).exists(): #enforce unique usernames
        return HttpResponse("Username is taken")

    user = User.objects.create_user(username=username)
    user.set_password(password)
    user.save()
    profile = Profile(user=user) #create profile for user
    profile.save()
    login(request, user)

    return redirect('index') #user will be logged in and sent to profile page

def signout(request):
    logout(request)

    return redirect('index')


@login_required(login_url='index')
def profile(request):
    currentuser = request.user
    if not hasattr(currentuser, 'profile'): #failsafe to ensure user definitely has profile
        Profile.objects.create(user=currentuser)
    thisprofile = Profile.objects.get(user=currentuser)

    #data for development section:
    keyskills = findKeySkills(currentuser)
    weakskills = findWeakSkills(currentuser)
    strongskills = findStrongSkills(currentuser)

    return render(request, "profile.html", {'profile': thisprofile, 'keyskills': keyskills, 'weakskills': weakskills, 'strongskills': strongskills})

@login_required(login_url='index')
def experiences(request):
    #fetch user experiences to send to template
    profile = Profile.objects.get(user=request.user)
    experiences = profile.experiences
    experienceform = ExperienceForm(profile=profile)

    return render(request, "experiences.html", { 'experiences': experiences, 'experienceform': experienceform })

@login_required(login_url='index')
def skills(request):
    # fetch user skills to send to template
    profile = Profile.objects.get(user=request.user)
    skills = profile.skills
    skillform = SkillForm()

    return render(request, "skills.html", { 'skills': skills, 'skillform': skillform })

@login_required(login_url='index')
def jobs(request):
    # fetch user jobs to send to template
    profile = Profile.objects.get(user=request.user)
    jobs = profile.jobs
    jobform = JobForm(profile=profile)

    return render(request, "jobs.html", { 'jobs': jobs, 'jobform': jobform })

@login_required(login_url='index')
def portfolio(request):
    # fetch user portfolio to send to template
    profile = Profile.objects.get(user=request.user)
    pieces = profile.portfoliopieces
    pieceform = PortfolioPieceForm(profile=profile)

    return render(request, "portfolio.html", { 'pieces': pieces, 'pieceform': pieceform })

@login_required(login_url='index')
def addExperience(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    experienceform = ExperienceForm(request.POST)
    if experienceform.is_valid():
        # add experience to user profile
        newexperience = experienceform.save()
        profile = Profile.objects.get(user=request.user)
        profile.experiences.add(Experience.objects.get(pk=newexperience.pk))
    else:
        return HttpResponse("Invalid form.")

    return redirect(experiences)

@login_required(login_url='index')
def addSkill(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    skillform = SkillForm(request.POST)
    if skillform.is_valid():
        # add skill to user profile
        # some users may share skills. to use less space, profiles reference the same skill entry
        if not Skill.objects.filter(title=skillform.cleaned_data['title']).exists():
            skillform.save()
        thisprofile = Profile.objects.get(user=request.user)
        thisprofile.skills.add(Skill.objects.get(title=skillform.cleaned_data['title']))
    else:
        return HttpResponse("Invalid form.")

    return redirect(skills)

@login_required(login_url='index')
def addJob(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    jobform = JobForm(request.POST)
    if jobform.is_valid():
        # add job to user profile
        newjob = jobform.save()
        profile = Profile.objects.get(user=request.user)
        profile.jobs.add(Job.objects.get(pk=newjob.pk))
    else:
        return HttpResponse("Invalid form.")

    return redirect(jobs)

@login_required(login_url='index')
def addPiece(request):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    pieceform = PortfolioPieceForm(request.POST, request.FILES)
    if pieceform.is_valid():
        # add piece to user profile
        newpiece = pieceform.save()
        profile = Profile.objects.get(user=request.user)
        profile.portfoliopieces.add(PortfolioPiece.objects.get(pk=newpiece.pk))
    else:
        return HttpResponse("Invalid form.")

    return redirect(portfolio)

@login_required(login_url='index')
def deleteExperience(request, id):
    Experience.objects.get(pk=id).delete()

    return redirect(experiences)

@login_required(login_url='index')
def deleteSkill(request, id):
    thisprofile = Profile.objects.get(user=request.user)
    thisprofile.skills.remove(Skill.objects.get(pk=id))

    # because users share rows in skills table, remove skill from user profile first
    # if no other users have the skill, it can be deleted
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
    # send experience information and edit form to template
    experience = Experience.objects.get(pk=id)
    if not experience:
        return HttpResponse("Experience not found.")

    profile = Profile.objects.get(user=request.user)
    experiences = profile.experiences.all()
    if not experiences.contains(experience):
        # do not allow users to edit other users' experiences
        return HttpResponse("Experience not found.")

    experienceform = ExperienceForm(instance=experience, profile=profile)

    return render(request, "editexperience.html", { 'experience': experience, 'experienceform': experienceform })

@login_required(login_url='index')
def editSkill(request, id):
    # send skill information and edit form to template
    skill = Skill.objects.get(pk=id)
    if not skill:
        return HttpResponse("Skill not found.")

    profile = Profile.objects.get(user=request.user)
    skills = profile.skills.all()
    if not skills.contains(skill):
        # do not allow users to edit other users' skills
        return HttpResponse("Skill not found.")

    skillform = SkillForm(instance=skill)
    return render(request, "editskill.html", { 'skill': skill, 'skillform': skillform })

@login_required(login_url='index')
def editJob(request, id):
    # send job information and edit form to template
    job = Job.objects.get(pk=id)
    if not job:
        return HttpResponse("Job not found.")

    profile = Profile.objects.get(user=request.user)
    jobs = profile.jobs.all()
    if not jobs.contains(job):
        # do not allow users to edit other users' jobs
        return HttpResponse("Job not found.")

    jobform = JobForm(instance=job, profile=profile)

    return render(request, "editjob.html", { 'job': job, 'jobform': jobform })

@login_required(login_url='index')
def editPiece(request, id):
    # send piece information and edit form to template
    piece = PortfolioPiece.objects.get(pk=id)
    if not piece:
        return HttpResponse("Piece not found.")

    profile = Profile.objects.get(user=request.user)
    pieces = profile.portfoliopieces.all()
    if not pieces.contains(piece):
        #do not allow users to edit other users' portfolios
        return HttpResponse("Piece not found.")

    pieceform = PortfolioPieceForm(instance=piece, profile=profile)

    return render(request, "editpiece.html", { 'piece': piece, 'pieceform': pieceform })

@login_required(login_url='index')
def experienceEdit(request, id):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    experience = Experience.objects.get(pk=id)

    # profile = Profile.objects.get(user=request.user)
    # experiences = profile.experiences.all()
    # if not experiences.contains(experience):
    #     # do not allow users to edit other users' experiences
    #     return HttpResponse("Experience not found.")

    experienceform = ExperienceForm(request.POST)
    if experienceform.is_valid():
        # save the new data
        experience.title = experienceform.cleaned_data['title']
        experience.description = experienceform.cleaned_data['description']
        experience.startdate = experienceform.cleaned_data['startdate']
        experience.enddate = experienceform.cleaned_data['enddate']
        experience.current = experienceform.cleaned_data['current']
        experience.skills.set(experienceform.cleaned_data['skills'])
        experience.save()
        return redirect(experiences)
    else:
        return HttpResponse("Invalid form.")

@login_required(login_url='index')
def skillEdit(request, id):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    skill = Skill.objects.get(pk=id)

    # profile = Profile.objects.get(user=request.user)
    # skills = profile.skills.all()
    # if not skills.contains(skill):
    #     # do not allow users to edit other users' skills
    #     return HttpResponse("Skill not found.")

    skillform = SkillForm(request.POST)
    if skillform.is_valid():
        # if only instance of skill, edit the instance
        profilecount = skill.profile.all().count()
        if profilecount == 1:
            skill.title = skillform.cleaned_data['title']
            skill.save()
            return redirect(skills)

        # if not only instance, remove from user's skills
        profile = Profile.objects.get(user=request.user)
        profile.skills.remove(Skill.objects.get(pk=id))

        # if skill from skillform exists, add to user skills
        if Skill.objects.filter(title=skillform.cleaned_data['title']).exists():
            profile.skills.add(Skill.objects.get(title=skillform.cleaned_data['title']))
            profile.save()
            return redirect(skills)

        # if skill does not exist, create new skill
        newskill = Skill(title=skillform.cleaned_data['title'])
        profile.skills.add(newskill)
        profile.save()
        return redirect(skills)

    return HttpResponse("Invalid form.")

@login_required(login_url='index')
def jobEdit(request, id):
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    job = Job.objects.get(pk=id)

    # profile = Profile.objects.get(user=request.user)
    # jobs = profile.jobs.all()
    # if not jobs.contains(job):
    #     # do not allow users to edit other users' jobs
    #     return HttpResponse("Job not found.")

    jobform = JobForm(request.POST)
    if jobform.is_valid():
        # save the new data
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
    if request.method != "POST":
        return HttpResponse("Invalid request.")

    piece = PortfolioPiece.objects.get(pk=id)

    # profile = Profile.objects.get(user=request.user)
    # pieces = profile.portfoliopieces.all()
    # if not pieces.contains(piece):
    #     # do not allow users to edit other users' portfolios
    #     return HttpResponse("Piece not found.")

    pieceform = PortfolioPieceForm(request.POST, request.FILES)
    if pieceform.is_valid():
        # save the new data
        piece.title = pieceform.cleaned_data['title']
        piece.description = pieceform.cleaned_data['description']
        piece.skills.set(pieceform.cleaned_data['skills'])

        # change image only if new one uploaded
        if 'image' in request.FILES:
            # user selected clear, remove image from database
            if 'image-clear' in request.POST:
                if piece.image:
                    img = piece.image.path
                    if os.path.exists(img):
                        os.remove(img)
                piece.image = None

            if piece.image:
                # if an image is already saved, remove it from database first
                oldimg = piece.image.path
                if os.path.exists(oldimg):
                    os.remove(oldimg)
            # save new image
            piece.image = request.FILES['image']

        piece.save()

        return redirect(portfolio)
    else:
        return HttpResponse("Invalid form.")

@login_required(login_url='index')
def buildResume(request, id):
    job = Job.objects.get(pk=id)
    profile = Profile.objects.get(user=request.user)
    jobs = profile.jobs.all()
    if not jobs.contains(job):
        # do not allow users to access other users' jobs
        return HttpResponse("Job not found.")

    experiences = []
    pieces = []
    for skill in job.skills.all():
        # collect experiences and portfolio pieces containing the same skills as the job
        relevantexperience = Experience.objects.filter(skills=skill)
        relevantpiece = PortfolioPiece.objects.filter(skills=skill)

        for experience in relevantexperience:
            if experience not in experiences:
                # ensure each experience is added once
                experiences.append(experience)
        for piece in relevantpiece:
            if piece not in pieces:
                # ensure each piece is added once
                pieces.append(piece)

    # sort experiences so most recent experiences are at the top
    experiences.sort(key=lambda experience: experience.startdate, reverse=True)

    # sort portfolio pieces by the number of skills they have in common with the job
    sortpieces = []
    similarity = []
    for piece in pieces:
        count = 0
        for skill in piece.skills.all():
            if skill in job.skills.all():
                count += 1
        similarity.append(count)

    for piece in pieces:
        # portfolio pieces with more relevant skills appear near the top
        index = similarity.index(max(similarity))
        currpiece = pieces[index]
        sortpieces.append(currpiece)
        similarity[index] = -1


    return render(request, 'buildresume.html', { 'experiences': experiences, 'pieces': sortpieces })

def skillSortByJobAppearance(user):
    # sort jobs by how often they appear in a user's saved jobs

    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    skills = profile.skills.all()
    priority = []
    priorityskills = []

    for skill in skills:
        # count how often the skill appears
        count = sum(skill in job.skills.all() for job in jobs)
        priority.append(count)

    for skill in skills:
        # order skills by frequency of appearance
        index = priority.index(max(priority))
        if priority[index] == 0:
            return priorityskills
        else:
            priorityskills.append(skills[index])
        # invalid value so skills aren't added more than once
        priority[index] = -1

    return priorityskills

def skillSortByExperienceAppearance(user):
    # sort skills by how often they appear in BOTH experiences and portfolio pieces COMBINED

    profile = Profile.objects.get(user=user)
    skills = profile.skills.all()
    experiences = profile.experiences.all()
    portfolio = profile.portfoliopieces.all()
    sortskill = []
    priority = []

    for skill in skills:
        # count how often skill appears in portfolio/experiences
        inexperience = sum(skill in experience.skills.all() for experience in experiences) + sum(skill in piece.skills.all() for piece in portfolio)
        priority.append(inexperience)
    for skill in skills:
        # order skills by frequency of appearance
        index = priority.index(max(priority))
        sortskill.append(skills[index])
        priority[index] = -1

    return sortskill

def findKeySkills(user):
    # return up to three skills that show up most often in a user's saved jobs

    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    skills = skillSortByJobAppearance(user)
    keyskills = []

    numkey = 3
    if numkey > len(skills):
        # if user does not have three skills, decrease number of key skills
        numkey = len(skills)

    # get top three skills
    for i in range(numkey):
        if sum(skills[i] in job.skills.all() for job in jobs) == 0:
            keyskills[i] = None
        else:
            keyskills.append(skills[i])

    return keyskills

def findWeakSkills(user):
    # return up to three skills that have largest difference between a user's saved jobs and saved experiences/portfolio pieces

    profile = Profile.objects.get(user=user)
    jobs = profile.jobs.all()
    experiences = profile.experiences.all()
    portfolio = profile.portfoliopieces.all()
    skills = skillSortByJobAppearance(user)

    numweak = 3
    if numweak > len(skills):
        # if user does not have three skills, decrease number of weak skills
        numweak = len(skills)
    weakskills = [None] * numweak
    priority = []

    for skill in skills:
        # count how often skills show up in jobs and experiences/portfolio
        injobs = sum(skill in job.skills.all() for job in jobs)
        inexperience = sum(skill in experience.skills.all() for experience in experiences) + sum(skill in piece.skills.all() for piece in portfolio)
        # find difference between
        priority.append(injobs - inexperience)

    # get bottom three skills
    for i in range(numweak):
        index = priority.index(max(priority))
        weakskills.append(skills[index])
        # make sure skills aren't added more than once
        priority[index] = min(priority) - 1

    return weakskills


def findStrongSkills(user):
    # return up to three skills that show up most in a user's saved experiences/portfolio pieces

    skills = skillSortByExperienceAppearance(user)
    numstrong = 3
    if numstrong > len(skills):
        # if user does not have three skills, decrease number of strong skills
        numstrong = len(skills)
    strongskills = [None] * numstrong

    # get top three skills
    for i in range(numstrong):
        strongskills[i] = skills[i]

    return strongskills