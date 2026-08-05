"""
apps/core/admin.py

Admin configuration for core models.
"""

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, Announcement


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    search_fields = ('name', 'codename')
    list_filter = ('content_type',)
    ordering = ('content_type__app_label', 'content_type__model', 'codename')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Singleton admin — prevents adding more than one instance.
    """

    fieldsets = (
        (_("Identity"), {
            'fields': ('site_name', 'site_short_name', 'tagline', 'logo', 'logo_dark', 'favicon'),
        }),
        (_("Contact Information"), {
            'fields': ('office_address', 'phone', 'email', 'membership_email', 'contact_email'),
        }),
        (_("Social Media"), {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url', 'whatsapp_number'),
            'classes': ('collapse',),
        }),
        (_("Footer"), {
            'fields': ('footer_about', 'copyright_text'),
        }),
        (_("Statistics"), {
            'fields': ('member_count', 'state_units_count', 'years_of_service'),
        }),
        (_("Analytics & SEO"), {
            'fields': ('google_analytics_id', 'google_search_console'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        """Allow adding only if no instance exists."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton."""
        return False


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_published', 'expires_at', 'order', 'created_at')
    list_filter = ('is_published', 'priority')
    list_editable = ('is_published', 'order', 'priority')
    search_fields = ('title', 'body')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', '-created_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'link', 'link_label', 'priority', 'order'),
        }),
        (_("Visibility"), {
            'fields': ('is_published', 'expires_at'),
        }),
        (_("Timestamps"), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
