from django.db import models

class CSVFile(models.Model):
    guide_csv_file = models.FileField(upload_to='csvs/') 
    student_csv_file = models.FileField(upload_to='csvs/')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.file.name
