"""
apps/search/views.py

Global site search across all major content types.
"""
from django.shortcuts import render
from django.db.models import Q

from apps.newsroom.models import NewsPost, PressRelease
from apps.people.models import OfficeBearer, StateUnit
from apps.documents.models import Document
from apps.events.models import Event


def search_results(request):
    q = request.GET.get('q', '').strip()
    results = {}
    total = 0

    if q:
        news = NewsPost.objects.filter(
            is_published=True
        ).filter(Q(title__icontains=q) | Q(summary__icontains=q))[:5]

        press = PressRelease.objects.filter(
            is_published=True
        ).filter(Q(title__icontains=q) | Q(summary__icontains=q))[:5]

        bearers = OfficeBearer.objects.filter(
            is_published=True
        ).filter(Q(name__icontains=q) | Q(role__icontains=q))[:5]

        states = StateUnit.objects.filter(
            is_published=True
        ).filter(Q(name__icontains=q) | Q(description__icontains=q))[:5]

        documents = Document.objects.filter(
            is_published=True
        ).filter(Q(title__icontains=q) | Q(description__icontains=q))[:5]

        events = Event.objects.filter(
            is_published=True
        ).filter(Q(title__icontains=q) | Q(location__icontains=q))[:5]

        results = {
            'news': news,
            'press': press,
            'bearers': bearers,
            'states': states,
            'documents': documents,
            'events': events,
        }
        total = sum(r.count() for r in results.values())

    return render(request, 'search/results.html', {
        'query': q,
        'results': results,
        'total': total,
        'breadcrumbs': [('Search', None)],
        'page_title': f'Search: {q}' if q else 'Search',
    })
