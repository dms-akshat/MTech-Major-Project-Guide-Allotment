from django.db import models

# Create your models here.
from my_admin_app.models import Student,Guide
from allocate.models import PreferenceOrder


class AllocatedGuide(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)

