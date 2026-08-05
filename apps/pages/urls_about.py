from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.about_index, name='index'),
    path('history/', views.about_history, name='history'),
    path('constitution/', views.about_constitution, name='constitution'),
    path('affiliations/', views.about_affiliations, name='affiliations'),
]
