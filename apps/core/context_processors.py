"""
apps/core/context_processors.py

Global template context injected into every request:
- site_settings: the SiteSettings singleton
- active_announcements: current announcements for the banner
- navigation: structured nav items for header/footer
"""

from django.utils import timezone
from django.db.models import Q
from .models import SiteSettings, Announcement


def site_settings(request):
    """
    Inject SiteSettings singleton into all templates.
    Cached on the request object to avoid repeated DB hits per request.
    """
    if not hasattr(request, '_site_settings'):
        request._site_settings = SiteSettings.get()
    return {
        'site_settings': request._site_settings,
    }


def navigation(request):
    """
    Inject active announcements and navigation structure into all templates.
    """
    now = timezone.now()

    active_announcements = Announcement.objects.filter(
        is_published=True,
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=now)
    ).order_by('order', '-created_at')[:5]

    nav_items = [
        {'label': 'Home', 'label_hi': 'मुख्य पृष्ठ', 'url': '/', 'name': 'pages:home'},
        {
            'label': 'About',
            'label_hi': 'हमारे बारे में',
            'url': '/about/',
            'name': 'about:index',
            'children': [
                {'label': 'Who We Are', 'label_hi': 'हम कौन हैं', 'url': '/about/', 'name': 'about:index'},
                {'label': 'History', 'label_hi': 'इतिहास', 'url': '/about/history/', 'name': 'about:history'},
                {'label': 'Constitution', 'label_hi': 'संविधान', 'url': '/about/constitution/', 'name': 'about:constitution'},
                {'label': 'Affiliations', 'label_hi': 'संपर्क/संगठन', 'url': '/about/affiliations/', 'name': 'about:affiliations'},
            ],
        },
        {'label': 'Office Bearers', 'label_hi': 'कार्यालय धारक', 'url': '/office-bearers/', 'name': 'bearers:list'},
        {'label': 'City Units', 'label_hi': 'शहर इकाइयां', 'url': '/city-units/', 'name': 'states:list'},
        {
            'label': 'Newsroom',
            'label_hi': 'समाचार कक्ष',
            'url': '/newsroom/',
            'name': 'newsroom:index',
            'children': [
                {'label': 'News Updates', 'label_hi': 'समाचार अपडेट', 'url': '/newsroom/news/', 'name': 'newsroom:news_list'},
                {'label': 'Press Releases', 'label_hi': 'प्रेस विज्ञप्ति', 'url': '/newsroom/press-releases/', 'name': 'newsroom:press_list'},
                {'label': 'Letters & Statements', 'label_hi': 'पत्र एवं बयान', 'url': '/newsroom/letters/', 'name': 'newsroom:letters_list'},
                {'label': 'Media Gallery', 'label_hi': 'मीडिया गैलरी', 'url': '/newsroom/gallery/', 'name': 'newsroom:gallery'},
            ],
        },
        {'label': 'Documents', 'label_hi': 'दस्तावेज़', 'url': '/documents/', 'name': 'documents:list'},
        {'label': 'Events', 'label_hi': 'कार्यक्रम', 'url': '/events/', 'name': 'events:list'},
        {
            'label': 'Membership',
            'label_hi': 'सदस्यता',
            'url': '/membership/',
            'name': 'membership:info',
            'children': [
                {'label': 'Membership Info', 'label_hi': 'सदस्यता जानकारी', 'url': '/membership/', 'name': 'membership:info'},
                {'label': 'Apply for Membership', 'label_hi': 'आवेदन करें', 'url': '/membership/apply/', 'name': 'membership:apply'},
                {'label': 'Member Directory', 'label_hi': 'सदस्य निर्देशिका', 'url': '/membership/directory/', 'name': 'membership:member_grid'},
                {'label': 'Check Status', 'label_hi': 'स्थिति जांचें', 'url': '/membership/status/', 'name': 'membership:status'},
            ],
        },
        {'label': 'Contact', 'label_hi': 'संपर्क', 'url': '/contact/', 'name': 'contact:index'},
    ]

    return {
        'active_announcements': active_announcements,
        'nav_items': nav_items,
    }
