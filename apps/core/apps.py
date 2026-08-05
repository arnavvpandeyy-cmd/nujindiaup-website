import copy as _copy_module
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core / Site Settings'

    def ready(self):
        """
        Apply compatibility patches for Python 3.14 + Django 5.0.

        In Python 3.14, copy.copy(super()) returns the super() proxy itself
        instead of a proper object copy. Django 5.0's BaseContext.__copy__
        uses copy(super()) which causes:
            AttributeError: 'super' object has no attribute 'dicts'
        This patch replaces __copy__ with a version that copies __dict__ directly.
        """
        self._patch_django_context_copy()
        self._patch_newsroom_admin()

    @staticmethod
    def _patch_django_context_copy():
        try:
            from django.template.context import BaseContext

            def _fixed_copy(self):
                """Python 3.14-safe copy for Django BaseContext."""
                duplicate = object.__new__(type(self))
                for key, val in self.__dict__.items():
                    try:
                        setattr(duplicate, key, _copy_module.copy(val))
                    except Exception:
                        setattr(duplicate, key, val)
                return duplicate

            BaseContext.__copy__ = _fixed_copy
        except Exception:
            pass  # If Django isn't ready yet, skip silently

    @staticmethod
    def _patch_newsroom_admin():
        """Remove emoji from fieldset names to avoid lazy-string copy issues."""
        try:
            from apps.newsroom.admin import NewsPostAdmin, PressReleaseAdmin
            # Replace fieldsets with plain string names (no gettext_lazy + emoji)
            NewsPostAdmin.fieldsets = (
                ("Content", {'fields': ('title', 'slug', 'category', 'author', 'summary', 'body')}),
                ("Cover Image", {'fields': ('cover_preview', 'cover_image')}),
                ("Publication", {'fields': ('is_published', 'is_featured', 'published_at')}),
                ("SEO", {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
                ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
            )
            PressReleaseAdmin.fieldsets = (
                ("Content", {'fields': ('title', 'slug', 'summary', 'body')}),
                ("Cover Image", {'fields': ('cover_preview', 'cover_image')}),
                ("Attachment", {'fields': ('attachment_link', 'attachment')}),
                ("Publication", {'fields': ('is_published', 'published_at')}),
                ("SEO", {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
            )
        except Exception:
            pass
