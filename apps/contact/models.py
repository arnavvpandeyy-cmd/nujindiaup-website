"""
apps/contact/models.py
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimestampedModel


class ContactInquiry(TimestampedModel):
    """Incoming contact form submission."""
    DEPARTMENT_CHOICES = [
        ('general', 'General Inquiry'),
        ('membership', 'Membership'),
        ('press', 'Press / Media'),
        ('legal', 'Legal / Grievance'),
        ('events', 'Events'),
        ('state_unit', 'State Unit Query'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES,
        default='general',
        verbose_name=_("Department / Subject")
    )
    subject = models.CharField(max_length=300, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    is_resolved = models.BooleanField(default=False, verbose_name=_("Resolved"))
    admin_notes = models.TextField(blank=True, verbose_name=_("Admin Notes"))

    class Meta:
        verbose_name = _("Contact Inquiry")
        verbose_name_plural = _("Contact Inquiries")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"
