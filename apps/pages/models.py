"""
apps/pages/models.py

Models for static CMS pages (About, etc.), HomeSections, and Testimonials.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.ck_field import CKEditor5Field
from apps.core.models import TimestampedModel, SEOFields


class StaticPage(TimestampedModel, SEOFields):
    """
    CMS-managed static pages (e.g., About, History, Constitution).
    """
    PAGE_KEYS = [
        ('about', 'About NUJ India'),
        ('history', 'History'),
        ('constitution', 'Constitution'),
        ('affiliations', 'Affiliations & Recognition'),
        ('vision_mission', 'Vision & Mission'),
    ]

    key = models.CharField(
        max_length=50,
        unique=True,
        choices=PAGE_KEYS,
        verbose_name=_("Page Key"),
        help_text=_("Unique identifier — links this record to a URL.")
    )
    title = models.CharField(max_length=300, verbose_name=_("Page Title"))
    subtitle = models.CharField(max_length=500, blank=True, verbose_name=_("Subtitle / Intro"))
    body = CKEditor5Field(config_name='default', verbose_name=_("Body Content"))
    cover_image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name=_("Cover Image"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Static Page")
        verbose_name_plural = _("Static Pages")
        ordering = ['order']

    def __str__(self):
        return self.title


class HomeSection(TimestampedModel):
    """
    Configurable homepage sections: hero, stats bar, message blocks, etc.
    """
    SECTION_TYPES = [
        ('hero', 'Hero Banner'),
        ('announcement_ticker', 'Announcement Ticker'),
        ('stats', 'Stats Bar'),
        ('news_press', 'News & Press Releases'),
        ('leadership_message', 'Leadership Message'),
        ('quick_links', 'Quick Links'),
        ('events', 'Upcoming Events'),
        ('documents', 'Important Documents'),
    ]

    section_type = models.CharField(
        max_length=50,
        choices=SECTION_TYPES,
        unique=True,
        verbose_name=_("Section Type")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    # Hero-specific fields
    hero_title = models.CharField(max_length=300, blank=True, verbose_name=_("Hero Title"))
    hero_subtitle = models.TextField(blank=True, verbose_name=_("Hero Subtitle / Mission Statement"))
    hero_cta_label = models.CharField(max_length=100, blank=True, default="Apply for Membership", verbose_name=_("Primary CTA Label"))
    hero_cta_url = models.CharField(max_length=200, blank=True, default="/membership/", verbose_name=_("Primary CTA URL"))
    hero_secondary_cta_label = models.CharField(max_length=100, blank=True, verbose_name=_("Secondary CTA Label"))
    hero_secondary_cta_url = models.CharField(max_length=200, blank=True, verbose_name=_("Secondary CTA URL"))
    hero_image = models.ImageField(upload_to='home/hero/', blank=True, null=True, verbose_name=_("Hero Background Image"))

    # Leadership message fields
    message_author_name = models.CharField(max_length=200, blank=True, verbose_name=_("Message Author Name"))
    message_author_role = models.CharField(max_length=200, blank=True, verbose_name=_("Message Author Role"))
    message_author_photo = models.ImageField(upload_to='home/messages/', blank=True, null=True, verbose_name=_("Author Photo"))
    message_body = models.TextField(blank=True, verbose_name=_("Message Body (excerpt)"))
    message_link = models.CharField(max_length=200, blank=True, verbose_name=_("Read Full Message Link"))

    class Meta:
        verbose_name = _("Home Section")
        verbose_name_plural = _("Home Sections")
        ordering = ['order']

    def __str__(self):
        return f"{self.get_section_type_display()} (order: {self.order})"


class Testimonial(TimestampedModel):
    """
    Quotes / testimonials from members or leaders shown on homepage or about page.
    """
    author_name = models.CharField(max_length=200, verbose_name=_("Author Name"))
    author_role = models.CharField(max_length=200, blank=True, verbose_name=_("Role / Designation"))
    author_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name=_("Photo"))
    quote = models.TextField(verbose_name=_("Quote"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['order']

    def __str__(self):
        return f"{self.author_name} — {self.author_role}"


class HomeSlide(TimestampedModel):
    """
    Homepage Hero Banner Slideshow Photos uploaded directly by Super Admin.
    """
    title = models.CharField(max_length=300, verbose_name=_("Slide Caption / Title"))
    image = models.ImageField(upload_to='home/slides/', verbose_name=_("Slide Photo / Image"))
    link = models.CharField(max_length=500, blank=True, verbose_name=_("Target Link (Optional)"))
    is_published = models.BooleanField(default=True, verbose_name=_("Active / Published"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Hero Slideshow Photo")
        verbose_name_plural = _("Hero Slideshow Photos")
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

