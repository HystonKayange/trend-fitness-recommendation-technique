from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser
#from user.models import Profile


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
