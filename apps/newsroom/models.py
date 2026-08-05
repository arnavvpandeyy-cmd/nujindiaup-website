"""
apps/newsroom/models.py

Models for:
- NewsCategory: Tag-like category for news posts
- NewsPost: General news updates / articles
- PressRelease: Official press releases
- LetterStatement: Letters addressed to govt/institutions
- MediaAsset: Photo gallery items
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from apps.core.ck_field import CKEditor5Field
from apps.core.models import TimestampedModel, SEOFields


class NewsCategory(models.Model):
    """Category for news posts."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    color = models.CharField(
        max_length=20,
        blank=True,
        default='#1a2744',
        verbose_name=_("Color (hex)"),
        help_text=_("e.g. #c0392b — used as label color.")
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsPost(TimestampedModel, SEOFields):
    """General news update or article."""
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    slug = models.SlugField(max_length=320, unique=True, blank=True, verbose_name=_("Slug"))
    summary = models.TextField(
        max_length=400,
        blank=True,
        verbose_name=_("Summary"),
        help_text=_("Short excerpt shown in list view. Max 400 characters.")
    )
    body = CKEditor5Field(config_name='default', verbose_name=_("Body"))
    cover_image = models.ImageField(upload_to='newsroom/news/', blank=True, null=True, verbose_name=_("Cover Image"))
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_posts',
        verbose_name=_("Category")
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Publish Date")
    )
    is_published = models.BooleanField(default=False, verbose_name=_("Published"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured on Homepage"))
    author = models.CharField(max_length=200, blank=True, verbose_name=_("Author Name"))

    class Meta:
        verbose_name = _("News Post")
        verbose_name_plural = _("News Posts")
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class NewsPostImage(models.Model):
    """Additional images for a news post (photo gallery / multiple images)."""
    post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='extra_images',
        verbose_name=_("News Post")
    )
    image = models.ImageField(
        upload_to='newsroom/news/gallery/',
        verbose_name=_("Image")
    )
    caption = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Caption")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("News Post Image")
        verbose_name_plural = _("News Post Images")
        ordering = ['order']

    def __str__(self):
        return f"{self.post.title} — Image {self.order}"


class PressRelease(TimestampedModel, SEOFields):
    """Official press release issued by NUJ India."""
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    summary = models.TextField(max_length=400, blank=True, verbose_name=_("Summary"))
    body = CKEditor5Field(config_name='default', verbose_name=_("Body"))
    cover_image = models.ImageField(upload_to='newsroom/press/', blank=True, null=True, verbose_name=_("Cover Image"))
    attachment = models.FileField(
        upload_to='newsroom/press/attachments/',
        blank=True,
        null=True,
        verbose_name=_("Attachment (PDF)"),
        help_text=_("Upload a PDF version of the press release.")
    )
    published_at = models.DateTimeField(default=timezone.now, verbose_name=_("Publish Date"))
    is_published = models.BooleanField(default=False, verbose_name=_("Published"))

    class Meta:
        verbose_name = _("Press Release")
        verbose_name_plural = _("Press Releases")
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class LetterStatement(TimestampedModel):
    """
    Official letters or statements addressed to government bodies,
    media organizations, or institutions.
    """
    title = models.CharField(max_length=300, verbose_name=_("Title"))
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    addressed_to = models.CharField(max_length=300, blank=True, verbose_name=_("Addressed To"))
    body = CKEditor5Field(config_name='default', verbose_name=_("Body / Content"))
    attachment = models.FileField(
        upload_to='newsroom/letters/',
        blank=True,
        null=True,
        verbose_name=_("Attachment")
    )
    date_issued = models.DateField(verbose_name=_("Date Issued"))
    is_published = models.BooleanField(default=False, verbose_name=_("Published"))

    class Meta:
        verbose_name = _("Letter / Statement")
        verbose_name_plural = _("Letters & Statements")
        ordering = ['-date_issued']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MediaAsset(TimestampedModel):
    """Photo gallery item."""
    GALLERY_CATEGORIES = [
        ('event', 'Event'),
        ('meeting', 'Meeting / Conference'),
        ('press', 'Press Activity'),
        ('award', 'Award / Recognition'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    image = models.ImageField(upload_to='newsroom/gallery/', verbose_name=_("Image"))
    caption = models.CharField(max_length=300, blank=True, verbose_name=_("Caption"))
    category = models.CharField(max_length=20, choices=GALLERY_CATEGORIES, default='other', verbose_name=_("Category"))
    upload_date = models.DateField(auto_now_add=True, verbose_name=_("Upload Date"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Media Asset")
        verbose_name_plural = _("Media Gallery")
        ordering = ['-upload_date', 'order']

    def __str__(self):
        return self.title
