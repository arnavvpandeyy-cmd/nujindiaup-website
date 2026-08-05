from django.urls import path
from . import views

app_name = 'newsroom'

urlpatterns = [
    path('', views.newsroom_index, name='index'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('press-releases/', views.press_list, name='press_list'),
    path('press-releases/<slug:slug>/', views.press_detail, name='press_detail'),
    path('letters/', views.letters_list, name='letters_list'),
    path('letters/<slug:slug>/', views.letter_detail, name='letter_detail'),
    path('gallery/', views.gallery, name='gallery'),
]
