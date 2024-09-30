# urls.py
from django.urls import path
from .views import login_view, otp_view, student_page, faculty_page, admin_page, logout_view, change_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('otp/<str:email>/', otp_view, name='otp_view'),
    path('student/<str:email>/', student_page, name='student_page'),
    path('faculty/<str:email>/', faculty_page, name='faculty_page'),
    path('admin/<str:email>/', admin_page, name='admin_page'),
    path('logout/', logout_view, name='logout_view'),  
    path('change_password/<str:email>/', change_password_view, name='change_password_view'),
]
