from django.urls import path
from .views import *
from . import api_views
urlpatterns = [
    path('<str:email>', upload_csv, name='upload_csv'),
    path('csv-files/<str:email>', csv_file_list, name='csv_file_list'),
    path('download_csv/<str:file_type>/<str:email>', download_csv, name='download_csv'),
    path('api/upload-csv/', api_views.UploadCSVAPI.as_view(), name='upload_csv_api'),
    path('api/download-csv/<str:file_type>/', api_views.DownloadCSVAPI.as_view(), name='download_csv_api'),
]
