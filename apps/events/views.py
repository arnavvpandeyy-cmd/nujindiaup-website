from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Event


def event_list(request):
    now = timezone.now()
    upcoming = Event.objects.filter(is_published=True, start_datetime__gte=now).order_by('start_datetime')
    past = Event.objects.filter(is_published=True, start_datetime__lt=now).order_by('-start_datetime')[:10]

    return render(request, 'events/list.html', {
        'upcoming': upcoming,
        'past': past,
        'breadcrumbs': [('Events', None)],
        'page_title': 'Events',
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    speakers = event.speakers.all().order_by('order')
    return render(request, 'events/detail.html', {
        'event': event,
        'speakers': speakers,
        'breadcrumbs': [('Events', '/events/'), (event.title, None)],
        'page_title': event.title,
    })
