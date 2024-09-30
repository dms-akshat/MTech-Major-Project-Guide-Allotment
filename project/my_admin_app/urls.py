from django.urls import path,include
from .views import upload_csv,  csv_file_list
from authentication.views import admin_page
urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('csv-files/', csv_file_list, name='csv_file_list'),
    path('auth/admin',admin_page, name='admin_page')
]
