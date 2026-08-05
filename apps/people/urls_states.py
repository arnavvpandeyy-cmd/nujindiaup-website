from django.urls import path
from . import views

app_name = 'states'

urlpatterns = [
    path('', views.state_unit_list, name='list'),
    path('<slug:slug>/', views.state_unit_detail, name='detail'),
]
