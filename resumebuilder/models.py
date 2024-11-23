from django.db import models
from django.utils import timezone

# Create your models here.

class Experience(models.Model):
    title = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    # startyear = models.IntegerField()
    # startmonth = models.IntegerField()
    # endyear = models.IntegerField()
    # endmonth = models.IntegerField()
    current = models.BooleanField()
    description = models.TextField(max_length=500)