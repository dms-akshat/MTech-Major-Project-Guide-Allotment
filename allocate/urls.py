# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check_eligibility/<int:student_id>/', views.check_eligibility, name='check_eligibility'),
    path('fill_preference_order/<int:student_id>/', views.fill_preference_order, name='fill_preference_order'),
    path('show_allocated_guide/<int:student_id>/', views.show_allocated_guide, name='show_allocated_guide'),
    # path('not_eligible/', views.not_eligible, name='show_allocated_guide'),
]
