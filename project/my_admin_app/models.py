from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='csvs/', null=True, blank=True)  # Allow null values
    start_date = models.DateField()
    end_date = models.DateField()

def __str__(self):
    # Return only the file's name (without the directory structure)
    return os.path.basename(self.file.name)