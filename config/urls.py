"""
NUJ India — Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap

# Sitemaps — graceful import
try:
    from apps.core.sitemaps import (
        StaticViewSitemap,
        NewsSitemap,
        PressReleaseSitemap,
        OfficeBearerSitemap,
        StateUnitSitemap,
        EventSitemap,
        DocumentSitemap,
    )
    sitemaps = {
        'static': StaticViewSitemap,
        'news': NewsSitemap,
        'press_releases': PressReleaseSitemap,
        'office_bearers': OfficeBearerSitemap,
        'city_units': StateUnitSitemap,
        'events': EventSitemap,
        'documents': DocumentSitemap,
    }
except ImportError:
    sitemaps = {}

admin_url = getattr(settings, 'ADMIN_URL', 'nuj-admin/')


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /nuj-admin/",
        "Disallow: /media/membership/",
        f"Sitemap: {getattr(settings, 'SITE_URL', 'http://localhost:8000')}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    # Admin
    path(admin_url, admin.site.urls),

    # Public apps
    path('', include('apps.pages.urls', namespace='pages')),
    path('about/', include('apps.pages.urls_about', namespace='about')),
    path('office-bearers/', include('apps.people.urls_bearers', namespace='bearers')),
    path('city-units/', include('apps.people.urls_states', namespace='states')),
    path('newsroom/', include('apps.newsroom.urls', namespace='newsroom')),
    path('documents/', include('apps.documents.urls', namespace='documents')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('membership/', include('apps.membership.urls', namespace='membership')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('portal/', include('apps.portal.urls', namespace='portal')),
    path('search/', include('apps.search.urls', namespace='search')),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

# CKEditor 5 URLs — only if installed
try:
    import django_ckeditor_5  # noqa: F401
    urlpatterns += [path('ckeditor5/', include('django_ckeditor_5.urls'), name='ck_editor_5_upload_file')]
except ImportError:
    pass

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
