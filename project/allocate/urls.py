# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check_eligibility/<str:email>/', views.check_eligibility, name='check_eligibility'),
    path('fill_preference_order/<str:email>/', views.fill_preference_order, name='fill_preference_order'),
    path('show_allocated_guide/<str:email>/', views.show_allocated_guide, name='show_allocated_guide'),
    path('preference_filled_no_guide_yet/<str:email>/', views.preference_filled_no_guide_yet, name='preference_filled_no_guide_yet'),
    # path('not_eligible/', views.not_eligible, name='show_allocated_guide'),
]
