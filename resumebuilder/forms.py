from django import forms
from .models import Experience, Skill, Job
from django.utils import timezone
from django.forms.widgets import CheckboxSelectMultiple

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        # widgets = {
        #     'skill': CheckboxSelectMultiple(),
        # }

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.current == True:
            self.fields['enddate'].disabled = True
            self.fields['enddate'].required = False

        self.fields['skills'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # Save many-to-many relationships

        def save_m2m():
            instance.skills.clear()
            instance.skills.add(*self.cleaned_data['skills'])

        return instance

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].required = False
        self.fields['link'].required = False
        self.fields['notes'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # Save many-to-many relationships

        def save_m2m():
            instance.skills.clear()
            instance.skills.add(*self.cleaned_data['skills'])

        return instance