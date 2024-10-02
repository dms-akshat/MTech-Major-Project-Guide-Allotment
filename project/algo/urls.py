from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("status/<str:email>", views.status, name="status"),
    path("generate_report/<str:email>",views.generate_report, name="generate_report")   
]


