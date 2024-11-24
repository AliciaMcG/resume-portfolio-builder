from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('experiences', views.experiences, name='experiences'),
    path('skills', views.skills, name='skills'),
    path('addexperience/', views.addExperience, name='addexperience'),
    path('addskill/', views.addSkill, name='addskill'),
    path('deleteexperience/<int:id>/', views.deleteExperience, name='deleteexperience'),
    path('deleteskill/<int:id>/', views.deleteSkill, name='deleteskill'),
]