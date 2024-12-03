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

class Job(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=500, null=True)
    notes = models.TextField(max_length=1000, null=True)
    skills = models.ManyToManyField(Skill, blank=True)