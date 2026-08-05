from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    # Public pages
    path('', views.membership_info, name='info'),
    path('directory/', views.public_member_grid, name='member_grid'),
    path('apply/', views.membership_apply, name='apply'),
    path('apply/success/<str:ref>/', views.membership_success, name='success'),
    path('status/', views.membership_status, name='status'),

    # Member portal — auth
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),

    # Member portal — dashboard
    path('portal/', views.member_dashboard, name='dashboard'),
    path('portal/edit/', views.member_profile_edit, name='profile_edit'),
    path('portal/card/', views.member_card, name='card'),
    path('portal/change-password/', views.change_password, name='change_password'),
]
