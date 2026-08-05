"""
apps/core/models.py

Core models: SiteSettings (singleton), SEOFields mixin, TimestampedModel mixin.
These provide foundational data structures used across all apps.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.ck_field import CKEditor5Field


class TimestampedModel(models.Model):
    """
    Abstract base model that adds created_at and updated_at timestamps
    to every model that inherits from it.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class SEOFields(models.Model):
    """
    Abstract mixin providing SEO metadata fields.
    Attach to any model that needs per-page SEO control.
    """
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        verbose_name=_("SEO Title"),
        help_text=_("Page title for search engines. Max 70 characters.")
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Meta Description"),
        help_text=_("Page description for search engines. Max 160 characters.")
    )
    og_image = models.ImageField(
        upload_to='seo/og/',
        blank=True,
        null=True,
        verbose_name=_("OG Image"),
        help_text=_("Open Graph image shown when shared on social media. Recommended: 1200x630px.")
    )

    class Meta:
        abstract = True


class SiteSettings(TimestampedModel):
    """
    Singleton model to store global site configuration.
    Managed from Django admin. Only one instance should exist.
    """
    # Identity
    site_name = models.CharField(
        max_length=200,
        default="National Union of Journalists (Uttar Pradesh)",
        verbose_name=_("Site Name")
    )
    site_short_name = models.CharField(
        max_length=50,
        default="NUJ UP",
        verbose_name=_("Short Name")
    )
    tagline = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Tagline"),
        help_text=_("One-line mission/tagline shown in hero and metadata.")
    )
    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name=_("Logo")
    )
    logo_dark = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name=_("Logo (Dark Mode)"),
        help_text=_("Alternate logo for dark backgrounds.")
    )
    favicon = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name=_("Favicon")
    )

    # Contact
    office_address = models.TextField(blank=True, verbose_name=_("Office Address"))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("General Email"))
    membership_email = models.EmailField(blank=True, verbose_name=_("Membership Email"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Contact Email"))

    # Social links
    facebook_url = models.URLField(blank=True, verbose_name=_("Facebook URL"))
    twitter_url = models.URLField(blank=True, verbose_name=_("Twitter/X URL"))
    instagram_url = models.URLField(blank=True, verbose_name=_("Instagram URL"))
    youtube_url = models.URLField(blank=True, verbose_name=_("YouTube URL"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn URL"))
    whatsapp_number = models.CharField(max_length=20, blank=True, verbose_name=_("WhatsApp Number"))

    # Footer
    footer_about = models.TextField(
        blank=True,
        verbose_name=_("Footer About Text"),
        help_text=_("Short description shown in footer.")
    )
    copyright_text = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Copyright Text")
    )

    # Membership numbers (for stats display)
    member_count = models.PositiveIntegerField(default=0, verbose_name=_("Total Members"))
    state_units_count = models.PositiveIntegerField(default=36, verbose_name=_("State Units"))
    years_of_service = models.PositiveIntegerField(default=0, verbose_name=_("Years of Service"))

    # Google Analytics / Search Console
    google_analytics_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Google Analytics ID"),
        help_text=_("e.g., G-XXXXXXXXXX")
    )
    google_search_console = models.TextField(
        blank=True,
        verbose_name=_("Google Search Console Verification"),
        help_text=_("Paste the full meta tag here.")
    )

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        """Enforce singleton — only one SiteSettings instance allowed."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        """Convenience method to fetch the singleton instance."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Announcement(TimestampedModel):
    """
    Site-wide announcements / notices displayed prominently on homepage.
    """
    PRIORITY_CHOICES = [
        ('normal', _('Normal')),
        ('important', _('Important')),
        ('urgent', _('Urgent')),
    ]

    title = models.CharField(max_length=300, verbose_name=_("Title"))
    body = models.TextField(blank=True, verbose_name=_("Body / Details"))
    link = models.URLField(blank=True, verbose_name=_("Link URL"), help_text=_("Optional: link this announcement to a page or document."))
    link_label = models.CharField(max_length=100, blank=True, default="Read More", verbose_name=_("Link Label"))
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name=_("Priority"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Expires At"), help_text=_("Auto-hide after this date. Leave blank to never expire."))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
