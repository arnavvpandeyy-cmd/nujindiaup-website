"""
apps/people/views.py

Views for Office Bearers and State Units.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import OfficeBearer, StateUnit, INDIAN_STATES


# ─── Office Bearers ───────────────────────────────────────────────────────────

def bearer_list(request):
    """
    Filterable directory of UP office bearers.
    """
    bearers = OfficeBearer.objects.filter(is_published=True, is_national=False).order_by('order', 'category', 'name')

    # Filter by category
    category = request.GET.get('category', '')
    if category:
        bearers = bearers.filter(category=category)

    # Filter by state
    state = request.GET.get('state', '')
    if state:
        bearers = bearers.filter(state=state)

    # Search
    q = request.GET.get('q', '')
    if q:
        bearers = bearers.filter(name__icontains=q) | bearers.filter(role__icontains=q)

    # Group by category for template display
    categories = OfficeBearer.CATEGORY_CHOICES
    states = INDIAN_STATES

    context = {
        'bearers': bearers,
        'categories': categories,
        'states': states,
        'selected_category': category,
        'selected_state': state,
        'query': q,
        'breadcrumbs': [('Office Bearers', None)],
        'page_title': 'UP Office Bearers',
        'heading_hi': 'यूपी कार्यालय धारक',
        'page_description': 'State-level leadership of NUJ Uttar Pradesh',
    }
    return render(request, 'people/bearer_list.html', context)


def national_bearer_list(request):
    """
    Filterable directory of national office bearers.
    """
    bearers = OfficeBearer.objects.filter(is_published=True, is_national=True).order_by('order', 'category', 'name')

    # Filter by category
    category = request.GET.get('category', '')
    if category:
        bearers = bearers.filter(category=category)

    # Filter by state
    state = request.GET.get('state', '')
    if state:
        bearers = bearers.filter(state=state)

    # Search
    q = request.GET.get('q', '')
    if q:
        bearers = bearers.filter(name__icontains=q) | bearers.filter(role__icontains=q)

    # Group by category for template display
    categories = OfficeBearer.CATEGORY_CHOICES
    states = INDIAN_STATES

    context = {
        'bearers': bearers,
        'categories': categories,
        'states': states,
        'selected_category': category,
        'selected_state': state,
        'query': q,
        'breadcrumbs': [('Office Bearers', None)],
        'page_title': 'National Office Bearers',
        'heading_hi': 'राष्ट्रीय कार्यालय धारक',
        'page_description': 'National leadership of NUJ India',
    }
    return render(request, 'people/bearer_list.html', context)


def bearer_detail(request, slug):
    """Individual office bearer profile page."""
    bearer = get_object_or_404(OfficeBearer, slug=slug, is_published=True)
    return render(request, 'people/bearer_detail.html', {
        'bearer': bearer,
        'breadcrumbs': [('Office Bearers', '/office-bearers/'), (bearer.name, None)],
        'page_title': bearer.name,
    })


# ─── State Units ─────────────────────────────────────────────────────────────

def state_unit_list(request):
    """Directory of all state units."""
    units = StateUnit.objects.filter(is_published=True).order_by('state')

    context = {
        'units': units,
        'breadcrumbs': [('State Units', None)],
        'page_title': 'State Units',
    }
    return render(request, 'people/state_list.html', context)


def state_unit_detail(request, slug):
    """Individual state unit profile page with its members."""
    unit = get_object_or_404(StateUnit, slug=slug, is_published=True)
    members = unit.members.all().order_by('order', 'name')

    context = {
        'unit': unit,
        'members': members,
        'breadcrumbs': [('State Units', '/state-units/'), (unit.name, None)],
        'page_title': unit.name,
    }
    return render(request, 'people/state_detail.html', context)
