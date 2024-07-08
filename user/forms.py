from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser, Profile
from .utils import *


class RegistrationForm(SignupForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data['username']
        user = CustomUser.objects.all().filter(username=username)
        if user.exists():
            raise forms.ValidationError('username "%s" is already in use.' % username)
        return username


class ProfileFormSection1(forms.ModelForm):

    primary_fitness_goal = forms.ChoiceField(choices=FITNESS_GOAL, widget=forms.RadioSelect())
    physical_activity_level = forms.ChoiceField(choices=PHYSICAL_ACTIVITY_LEVEL, widget=forms.RadioSelect())
    fitness_environment = forms.ChoiceField(choices=FITNESS_ENVIRONMENT, widget=forms.RadioSelect())


    class Meta:
        model = Profile
        fields = ('primary_fitness_goal', 'medical_history', 'nutritional_preferences', 'physical_activity_level')


class ProfileFormSection2(forms.ModelForm):

    fitness_environment = forms.ChoiceField(choices=FITNESS_ENVIRONMENT, widget=forms.RadioSelect())
    tracking_method = forms.ChoiceField(choices=TRACKING_METHOD, widget=forms.RadioSelect())
    time_commitment = forms.ChoiceField(choices=TIME_COMMITMENT, widget=forms.RadioSelect())


    class Meta:
        model = Profile
        fields = ('fitness_environment', 'tracking_method', 'time_commitment', 'challenges')

