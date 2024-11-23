from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addexperience/', views.addExperience, name='addexperience'),
    path('deleteexperience/<int:id>/', views.deleteExperience, name='deleteexperience'),
]