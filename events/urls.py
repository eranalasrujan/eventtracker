# C:\Users\91912\Documents\eventtracker\events\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('dashboard/sudha/', views.sudha_dashboard, name='sudha_dashboard'),
]
