from django.urls import path
from .views import *
urlpatterns = [
    path('<str:email>', upload_csv, name='upload_csv'),
    path('csv-files/<str:email>', csv_file_list, name='csv_file_list'),
    path('download_csv/<str:file_type>/<str:email>', download_csv, name='download_csv'),
]
