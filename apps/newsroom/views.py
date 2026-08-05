"""
apps/newsroom/views.py

Newsroom section: news posts, press releases, letters, gallery.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsPost, PressRelease, LetterStatement, MediaAsset, NewsCategory


def newsroom_index(request):
    """Newsroom landing page — overview of all content types."""
    latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_at')[:6]
    latest_press = PressRelease.objects.filter(is_published=True).order_by('-published_at')[:4]
    latest_letters = LetterStatement.objects.filter(is_published=True).order_by('-date_issued')[:3]

    return render(request, 'newsroom/index.html', {
        'latest_news': latest_news,
        'latest_press': latest_press,
        'latest_letters': latest_letters,
        'breadcrumbs': [('Newsroom', None)],
        'page_title': 'Newsroom',
    })


def news_list(request):
    """Paginated list of all news posts with category filter."""
    queryset = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    categories = NewsCategory.objects.all()

    category_slug = request.GET.get('category', '')
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    q = request.GET.get('q', '')
    if q:
        queryset = queryset.filter(title__icontains=q) | queryset.filter(summary__icontains=q)

    paginator = Paginator(queryset, 9)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'newsroom/news_list.html', {
        'page_obj': page,
        'categories': categories,
        'selected_category': category_slug,
        'query': q,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('News Updates', None)],
        'page_title': 'News Updates',
    })


def news_detail(request, slug):
    """Individual news post with gallery images."""
    post = get_object_or_404(
        NewsPost.objects.prefetch_related('extra_images'),
        slug=slug, is_published=True
    )
    related = NewsPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(pk=post.pk).order_by('-published_at')[:3]

    return render(request, 'newsroom/news_detail.html', {
        'post': post,
        'related': related,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('News Updates', '/newsroom/news/'), (post.title, None)],
        'page_title': post.seo_title or post.title,
    })


def press_list(request):
    """Paginated list of press releases."""
    queryset = PressRelease.objects.filter(is_published=True).order_by('-published_at')
    q = request.GET.get('q', '')
    if q:
        queryset = queryset.filter(title__icontains=q)

    paginator = Paginator(queryset, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'newsroom/press_list.html', {
        'page_obj': page,
        'query': q,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('Press Releases', None)],
        'page_title': 'Press Releases',
    })


def press_detail(request, slug):
    """Individual press release."""
    release = get_object_or_404(PressRelease, slug=slug, is_published=True)
    return render(request, 'newsroom/press_detail.html', {
        'release': release,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('Press Releases', '/newsroom/press-releases/'), (release.title, None)],
        'page_title': release.seo_title or release.title,
    })


def letters_list(request):
    """List of letters and statements."""
    queryset = LetterStatement.objects.filter(is_published=True).order_by('-date_issued')
    paginator = Paginator(queryset, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'newsroom/letters_list.html', {
        'page_obj': page,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('Letters & Statements', None)],
        'page_title': 'Letters & Statements',
    })


def letter_detail(request, slug):
    """Individual letter/statement."""
    letter = get_object_or_404(LetterStatement, slug=slug, is_published=True)
    return render(request, 'newsroom/letter_detail.html', {
        'letter': letter,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('Letters', '/newsroom/letters/'), (letter.title, None)],
        'page_title': letter.title,
    })


def gallery(request):
    """Media gallery."""
    assets = MediaAsset.objects.filter(is_published=True)
    category = request.GET.get('category', '')
    if category:
        assets = assets.filter(category=category)

    categories = MediaAsset.GALLERY_CATEGORIES
    paginator = Paginator(assets, 20)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'newsroom/gallery.html', {
        'page_obj': page,
        'categories': categories,
        'selected_category': category,
        'breadcrumbs': [('Newsroom', '/newsroom/'), ('Media Gallery', None)],
        'page_title': 'Media Gallery',
    })
