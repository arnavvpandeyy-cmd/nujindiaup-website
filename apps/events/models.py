"""
apps/events/models.py
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from apps.core.ck_field import CKEditor5Field
from apps.core.models import TimestampedModel, SEOFields


class Event(TimestampedModel, SEOFields):
    """Union events — conferences, meetings, award ceremonies, etc."""
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('meeting', 'General Meeting'),
        ('workshop', 'Workshop / Training'),
        ('award', 'Award / Recognition'),
        ('protest', 'Press / Protest'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300, verbose_name=_("Title"))
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    description = CKEditor5Field(config_name='default', verbose_name=_("Description"))
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES, default='other', verbose_name=_("Event Type"))
    location = models.CharField(max_length=300, blank=True, verbose_name=_("Location"))
    location_detail = models.TextField(blank=True, verbose_name=_("Location Details / Address"))
    start_datetime = models.DateTimeField(verbose_name=_("Start Date & Time"))
    end_datetime = models.DateTimeField(blank=True, null=True, verbose_name=_("End Date & Time"))
    cover_image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name=_("Cover Image"))
    registration_link = models.URLField(blank=True, verbose_name=_("Registration / RSVP Link"))
    is_published = models.BooleanField(default=False, verbose_name=_("Published"))

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        return self.start_datetime >= timezone.now()


class EventSpeaker(models.Model):
    """Guest or speaker at an event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    role = models.CharField(max_length=200, blank=True, verbose_name=_("Role / Organization"))
    bio = models.TextField(blank=True, verbose_name=_("Bio"))
    photo = models.ImageField(upload_to='event_speakers/', blank=True, null=True, verbose_name=_("Photo"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} @ {self.event.title}"
