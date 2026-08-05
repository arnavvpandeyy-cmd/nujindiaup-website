"""
apps/pages/views.py

Views for homepage and about section pages.
"""

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from apps.core.models import Announcement
from apps.pages.models import StaticPage, HomeSection, HomeSlide
from apps.newsroom.models import NewsPost, PressRelease
from apps.people.models import OfficeBearer
from apps.events.models import Event
from apps.documents.models import Document


def _ensure_homeslide_table():
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pages_homeslide (
                    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    title varchar(300) NOT NULL,
                    image varchar(100) NOT NULL,
                    link varchar(500) NOT NULL,
                    is_published boolean NOT NULL,
                    "order" integer unsigned NOT NULL CHECK ("order" >= 0)
                );
            """)
    except Exception:
        pass


def home(request):
    """
    Homepage view — assembles all homepage section data.
    """
    now = timezone.now()
    _ensure_homeslide_table()

    # Hero slides uploaded by Super Admin
    try:
        hero_slides = HomeSlide.objects.filter(is_published=True).order_by('order', '-created_at')
    except Exception:
        hero_slides = []

    # Hero / Home sections
    try:
        hero = HomeSection.objects.get(section_type='hero', is_active=True)
    except HomeSection.DoesNotExist:
        hero = None

    try:
        leader_message = HomeSection.objects.get(section_type='leadership_message', is_active=True)
    except HomeSection.DoesNotExist:
        leader_message = None

    # Latest news (10 items for slideshow fallback)
    latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_at')[:10]

    # Latest press releases (3 items)
    latest_press = PressRelease.objects.filter(is_published=True).order_by('-published_at')[:3]

    # Upcoming events (3 items)
    upcoming_events = Event.objects.filter(
        is_published=True,
        start_datetime__gte=now
    ).order_by('start_datetime')[:3]

    # Important documents (5 items)
    important_docs = Document.objects.filter(is_published=True, is_featured=True).order_by('-published_at')[:5]

    # National office bearers (featured — national roles)
    national_bearers = OfficeBearer.objects.filter(
        is_published=True, is_featured=True, is_national=True
    ).order_by('order')[:6]

    # UP office bearers (featured — president, sec gen, etc.)
    featured_bearers = OfficeBearer.objects.filter(
        is_published=True, is_featured=True, is_national=False
    ).order_by('order')[:6]

    # Announcements (from context processor — available globally)

    context = {
        'hero_slides': hero_slides,
        'hero': hero,
        'leader_message': leader_message,
        'latest_news': latest_news,
        'latest_press': latest_press,
        'upcoming_events': upcoming_events,
        'important_docs': important_docs,
        'national_bearers': national_bearers,
        'featured_bearers': featured_bearers,
        'page_title': 'Home',
    }
    return render(request, 'pages/home.html', context)


def about_index(request):
    """About NUJ UP — main page. Renders directly without requiring a DB StaticPage entry."""
    return render(request, 'pages/about.html', {
        'breadcrumbs': [('About', None)],
        'page_title': 'About NUJ UP — National Union of Journalists (Uttar Pradesh)',
    })



def about_history(request):
    """History page — renders directly without requiring a DB StaticPage entry."""
    return render(request, 'pages/static_page.html', {
        'page': {
            'title': 'History of NUJ UP',
            'content': '''<p>The National Union of Journalists (India) has a proud history spanning over six decades of fighting for press freedom and journalists' welfare. The Uttar Pradesh chapter has been an integral part of this movement, representing journalists across all 75 districts of the state.</p>
            <p>Founded to give working journalists a collective voice, NUJ India affiliated itself with the International Federation of Journalists (IFJ), Brussels — connecting Indian journalists to a global network of over 600,000 media professionals in 140+ countries.</p>
            <p>Over the decades, NUJ UP has stood firm in defence of press freedom, intervening in cases of journalist harassment, wrongful termination, and threats to media independence across Uttar Pradesh.</p>'''
        },
        'breadcrumbs': [('About', '/about/'), ('History', None)],
        'page_title': 'History — NUJ Uttar Pradesh',
    })


def about_constitution(request):
    """Constitution page — renders directly without requiring a DB StaticPage entry."""
    return render(request, 'pages/static_page.html', {
        'page': {
            'title': 'Constitution of NUJ UP',
            'content': '''<p>The National Union of Journalists (India) operates under a formal Constitution that governs the rights and responsibilities of all members, the election of office bearers, and the functioning of State and City Units.</p>
            <p>The Constitution upholds democratic principles — all office bearers at the national, state, and city level are elected by members. It guarantees freedom of expression within the union, transparency in finances, and the right of every member to seek redressal of grievances.</p>
            <p>For a copy of the full Constitution, please <a href="/contact/" class="text-union-red hover:underline">contact the NUJ UP Secretariat</a> or call us at <a href="tel:+917054000149" class="text-union-red hover:underline">+91 70540 00149</a>.</p>'''
        },
        'breadcrumbs': [('About', '/about/'), ('Constitution', None)],
        'page_title': 'Constitution — NUJ Uttar Pradesh',
    })


def about_affiliations(request):
    """Affiliations page — renders directly without requiring a DB StaticPage entry."""
    return render(request, 'pages/static_page.html', {
        'page': {
            'title': 'Affiliations & Recognition',
            'content': '''<p><strong>International Federation of Journalists (IFJ)</strong><br/>NUJ India is a proud affiliate of the IFJ — the world's largest journalists' organisation, headquartered in Brussels, Belgium. The IFJ represents over 600,000 journalists in more than 140 countries and campaigns for press freedom, journalists' safety, and professional standards globally.</p>
            <p><strong>Press Council of India</strong><br/>NUJ India is recognised by the Press Council of India, the statutory body that oversees the conduct and standards of the press in India.</p>
            <p><strong>National Press Day</strong><br/>NUJ India actively participates in National Press Day (November 16) each year, reaffirming its commitment to a free and responsible press.</p>'''
        },
        'breadcrumbs': [('About', '/about/'), ('Affiliations', None)],
        'page_title': 'Affiliations — NUJ Uttar Pradesh',
    })

