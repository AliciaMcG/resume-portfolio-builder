from django.shortcuts import render

from resumebuilder.models import Experience


# Create your views here.
def index(request):
    experiences = Experience.objects.all()
    return render(request, "index.html", { 'experiences': experiences })