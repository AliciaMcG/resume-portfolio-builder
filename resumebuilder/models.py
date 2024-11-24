from django.db import models
from django.utils import timezone

# Create your models here.

class Experience(models.Model):
    title = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    current = models.BooleanField()
    description = models.TextField(max_length=500)

class Skill(models.Model):
    title = models.CharField(max_length=100)