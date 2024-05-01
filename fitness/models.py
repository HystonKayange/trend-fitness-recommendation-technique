from django.db import models
from user.models import CustomUser

PHYSICAL_ACTIVITY_CHOICES = (
    ('LO', "low"),
    ('MO', "Moderate"),
    ('HI', "high"),
)

DIETARY_PREFERENCES_CHOICES =(
    ('BD', "Balanced Diet"),
    ('PRD', "Protein Diet"),
    ('VD', "Vegetarian Diet"),
    ('MD', "Mediterranean Diet"),
    ('GFD', "Gluten-Free Diet"),
    ('LCD', "Low Carb Diet"),
    ('PDD', "Plant-Based Diet"),
    ('PD', "Paleo Diet"),
    ('LFD', "Low Fat Diet"),
)


class FitnessGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    fitness_goals = models.CharField(max_length=100)
    medical_history = models.TextField(max_length=100)
    physical_activity_level = models.CharField(max_length=100)
    dietary_preferences = models.CharField(max_length=100)
