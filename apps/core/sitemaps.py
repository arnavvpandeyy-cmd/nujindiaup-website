"""
apps/core/sitemaps.py

XML sitemaps for all public-facing content.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'pages:home',
            'about:index',
            'bearers:list',
            'states:list',
            'newsroom:index',
            'documents:list',
            'events:list',
            'membership:info',
            'contact:index',
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        from apps.newsroom.models import NewsPost
        return NewsPost.objects.filter(is_published=True).order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('newsroom:news_detail', kwargs={'slug': obj.slug})


class PressReleaseSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        from apps.newsroom.models import PressRelease
        return PressRelease.objects.filter(is_published=True).order_by('-published_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('newsroom:press_detail', kwargs={'slug': obj.slug})


class OfficeBearerSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        from apps.people.models import OfficeBearer
        return OfficeBearer.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('bearers:detail', kwargs={'slug': obj.slug})


class StateUnitSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        from apps.people.models import StateUnit
        return StateUnit.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('states:detail', kwargs={'slug': obj.slug})


class EventSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        from apps.events.models import Event
        return Event.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('events:detail', kwargs={'slug': obj.slug})


class DocumentSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        from apps.documents.models import Document
        return Document.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('documents:detail', kwargs={'slug': obj.slug})
