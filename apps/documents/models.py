"""
apps/documents/models.py
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from apps.core.models import TimestampedModel


class DocumentCategory(models.Model):
    """Category for documents (Circular, Notice, Report, Policy, etc.)."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category"))
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text=_("Optional icon class name."))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Document Category")
        verbose_name_plural = _("Document Categories")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Document(TimestampedModel):
    """
    Downloadable document: circular, notice, report, policy, etc.
    """
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_("Category")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        verbose_name=_("File (PDF/DOC)"),
        help_text=_("Accepted: PDF, DOC, DOCX")
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Year"),
        help_text=_("Year of the document for filtering purposes.")
    )
    published_at = models.DateTimeField(default=timezone.now, verbose_name=_("Published Date"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured (shown on homepage)"))
    download_count = models.PositiveIntegerField(default=0, verbose_name=_("Download Count"), editable=False)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.year and self.published_at:
            self.year = self.published_at.year
        super().save(*args, **kwargs)
