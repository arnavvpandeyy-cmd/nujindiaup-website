"""
apps/core/ck_field.py

Provides a safe CKEditor5Field that falls back to TextField
when django-ckeditor-5 is not installed (e.g. in dev without it).

The fallback strips CKEditor-specific kwargs (config_name, etc.)
so models don't need to be changed.
"""
try:
    from django_ckeditor_5.fields import CKEditor5Field
except ImportError:
    from django.db.models import TextField

    class CKEditor5Field(TextField):  # type: ignore[no-redef]
        """
        Drop-in replacement for CKEditor5Field when the package is absent.
        Silently ignores CKEditor-specific kwargs like config_name.
        """
        def __init__(self, *args, **kwargs):
            # Strip kwargs that only CKEditor5Field understands
            kwargs.pop('config_name', None)
            kwargs.pop('extra_plugins', None)
            super().__init__(*args, **kwargs)

__all__ = ['CKEditor5Field']
