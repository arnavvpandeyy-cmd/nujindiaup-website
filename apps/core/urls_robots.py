"""
apps/core/urls_robots.py — robots.txt URL handler
"""
from django.urls import path
from django.http import HttpResponse
from django.conf import settings


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /nuj-admin/",
        "Disallow: /membership/apply/",
        "Disallow: /contact/",
        "Disallow: /search/",
        "",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path('', robots_txt, name='robots_txt'),
]
