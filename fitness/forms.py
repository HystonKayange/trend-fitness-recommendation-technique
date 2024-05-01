# forms.py
import django.forms as forms
from .models import FitnessGoal


class FitnessGoalsForm(forms.Form):

    class Meta:
        model = FitnessGoal
        fields = "__all__"
