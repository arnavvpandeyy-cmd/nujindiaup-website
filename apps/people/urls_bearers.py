from django.urls import path
from . import views

app_name = 'bearers'

urlpatterns = [
    path('', views.bearer_list, name='list'),
    path('national/', views.national_bearer_list, name='national'),
    path('<slug:slug>/', views.bearer_detail, name='detail'),
]
