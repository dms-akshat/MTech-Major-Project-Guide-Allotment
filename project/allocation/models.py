from django.db import models

# Create your models here.

class Student(models.Model):

    name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=30)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    pref_queue = models.JSONField(default=list)
    cluster = models.IntegerField()
    allotment_status = models.CharField(max_length=30)
    allotment = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

