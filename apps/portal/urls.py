from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Full custom admin panel (replaces Django admin index)
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # Super Admin
    path('admin/', views.super_admin_home, name='admin_home'),
    path('admin/members/', views.admin_members, name='admin_members'),
    path('admin/members/<int:pk>/edit/', views.admin_member_edit, name='admin_member_edit'),
    path('admin/applications/', views.admin_applications, name='admin_applications'),
    path('admin/applications/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
    path('admin/city-units/', views.admin_city_units, name='admin_city_units'),
    path('admin/city-units/add/', views.admin_city_unit_edit, name='admin_city_unit_add'),
    path('admin/city-units/<int:pk>/edit/', views.admin_city_unit_edit, name='admin_city_unit_edit'),
    path('admin/office-bearers/', views.admin_office_bearers, name='admin_office_bearers'),
    path('admin/office-bearers/add/', views.admin_bearer_edit, name='admin_bearer_add'),
    path('admin/office-bearers/<int:pk>/edit/', views.admin_bearer_edit, name='admin_bearer_edit'),
    path('admin/news/', views.admin_news, name='admin_news'),
    path('admin/news/add/', views.admin_news_edit, name='admin_news_add'),
    path('admin/news/<int:pk>/edit/', views.admin_news_edit, name='admin_news_edit'),
    path('admin/press-release/add/', views.admin_press_release_edit, name='admin_press_release_add'),
    path('admin/press-release/<int:pk>/edit/', views.admin_press_release_edit, name='admin_press_release_edit'),

    # Additional portal admin modules
    path('admin/contact/', views.admin_contact, name='admin_contact'),
    path('admin/documents/', views.admin_documents, name='admin_documents'),
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/site-settings/', views.admin_site_settings, name='admin_site_settings'),
    path('admin/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin/slides/', views.admin_slides, name='admin_slides'),

    # City Admin
    path('city-admin/', views.city_admin_home, name='city_admin_home'),
    path('city-admin/edit-unit/', views.city_admin_unit_edit, name='city_admin_unit_edit'),

    # Enhanced member city dashboard
    path('dashboard/', views.member_city_dashboard, name='member_city_dashboard'),
]
