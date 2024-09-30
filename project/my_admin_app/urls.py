from django.urls import path
from .views import upload_csv,  csv_file_list
urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('csv-files/', csv_file_list, name='csv_file_list'),
]
