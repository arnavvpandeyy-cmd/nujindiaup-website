"""
apps/documents/views.py
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Document, DocumentCategory


def document_list(request):
    queryset = Document.objects.filter(is_published=True).select_related('category').order_by('-published_at')

    # Filters
    category_slug = request.GET.get('category', '')
    year = request.GET.get('year', '')
    q = request.GET.get('q', '')

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    if year:
        queryset = queryset.filter(year=year)
    if q:
        queryset = queryset.filter(title__icontains=q)

    categories = DocumentCategory.objects.all()
    years = Document.objects.filter(is_published=True).values_list('year', flat=True).distinct().order_by('-year')

    paginator = Paginator(queryset, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'documents/list.html', {
        'page_obj': page,
        'categories': categories,
        'years': [y for y in years if y],
        'selected_category': category_slug,
        'selected_year': year,
        'query': q,
        'breadcrumbs': [('Documents', None)],
        'page_title': 'Documents & Circulars',
    })


def document_detail(request, slug):
    doc = get_object_or_404(Document, slug=slug, is_published=True)
    return render(request, 'documents/detail.html', {
        'doc': doc,
        'breadcrumbs': [('Documents', '/documents/'), (doc.title, None)],
        'page_title': doc.title,
    })


def document_download(request, slug):
    """Track download count and redirect to file URL."""
    doc = get_object_or_404(Document, slug=slug, is_published=True)
    Document.objects.filter(pk=doc.pk).update(download_count=doc.download_count + 1)
    return HttpResponseRedirect(doc.file.url)
