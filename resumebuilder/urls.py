from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('experiences', views.experiences, name='experiences'),
    path('skills', views.skills, name='skills'),
    path('jobs', views.jobs, name='jobs'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('addexperience/', views.addExperience, name='addexperience'),
    path('addskill/', views.addSkill, name='addskill'),
    path('addjob/', views.addJob, name='addjob'),
    path('addpiece/', views.addPiece, name='addpiece'),
    path('deleteexperience/<int:id>/', views.deleteExperience, name='deleteexperience'),
    path('deleteskill/<int:id>/', views.deleteSkill, name='deleteskill'),
    path('deletejob/<int:id>/', views.deleteJob, name='deletejob'),
    path('deletepiece/<int:id>/', views.deletePiece, name='deletepiece'),
    path('editskill/<int:id>/', views.editSkill, name='editskill'),
    path('editexperience/<int:id>/', views.editExperience, name='editexperience'),
    path('editjob/<int:id>/', views.editJob, name='editjob'),
    path('editpiece/<int:id>/', views.editPiece, name='editpiece'),
    path('skilledit/<int:id>/', views.skillEdit, name='skilledit'),
    path('experienceedit/<int:id>/', views.experienceEdit, name='experienceedit'),
    path('jobedit/<int:id>/', views.jobEdit, name='jobedit'),
    path('pieceedit/<int:id>/', views.pieceEdit, name='pieceedit'),
    path('buildresume/<int:id>/', views.buildResume, name='buildResume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)