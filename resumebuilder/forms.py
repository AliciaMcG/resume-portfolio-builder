from django import forms
from .models import Experience, Skill
from django.utils import timezone

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.current == True:
            self.fields['enddate'].disabled = True
            self.fields['enddate'].required = False

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'