from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Experience, Skill

admin.site.register(Experience)
admin.site.register(Skill)