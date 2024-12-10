from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('experiences', views.experiences, name='experiences'),
    path('skills', views.skills, name='skills'),
    path('jobs', views.jobs, name='jobs'),
    path('addexperience/', views.addExperience, name='addexperience'),
    path('addskill/', views.addSkill, name='addskill'),
    path('addjob/', views.addJob, name='addjob'),
    path('deleteexperience/<int:id>/', views.deleteExperience, name='deleteexperience'),
    path('deleteskill/<int:id>/', views.deleteSkill, name='deleteskill'),
    path('deletejob/<int:id>/', views.deleteJob, name='deletejob'),
    path('editskill/<int:id>/', views.editSkill, name='editskill'),
    path('editexperience/<int:id>/', views.editExperience, name='editexperience'),
    path('editjob/<int:id>/', views.editJob, name='editjob'),
    path('skilledit/<int:id>/', views.skillEdit, name='skilledit'),
    path('experienceedit/<int:id>/', views.experienceEdit, name='experienceedit'),
    path('jobedit/<int:id>/', views.jobEdit, name='jobedit'),
    path('buildresume/<int:id>/', views.buildResume, name='buildResume'),
]