# stats/urls.py
from django.urls import path
from .views import stats_dashboard_view

app_name = 'stats'

urlpatterns = [
    path('', stats_dashboard_view, name='dashboard'),
]