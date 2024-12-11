from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Skill(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Experience(models.Model):
    title = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    current = models.BooleanField()
    description = models.TextField(max_length=500)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title

class Job(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=500, blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title

class PortfolioPiece(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    skills = models.ManyToManyField(Skill, blank=True)
    image = models.ImageField(upload_to='portfolio_pictures', blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.ManyToManyField(Skill, blank=True, related_name='profile')
    experiences = models.ManyToManyField(Experience, blank=True, related_name='profile')
    jobs = models.ManyToManyField(Job, blank=True, related_name='profile')
    portfoliopieces = models.ManyToManyField(PortfolioPiece, blank=True, related_name='profile')

    def __str__(self):
        return self.user.username