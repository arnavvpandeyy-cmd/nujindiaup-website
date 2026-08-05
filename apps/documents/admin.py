from django.contrib import admin
from django.utils.html import format_html
from .models import DocumentCategory, Document


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'is_published', 'is_featured', 'download_count', 'file_link', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category', 'year')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('download_count', 'created_at', 'updated_at', 'file_link_detail')
    date_hierarchy = 'published_at'
    save_on_top = True
    fieldsets = (
        ("Document", {'fields': ('title', 'slug', 'category', 'description', 'file_link_detail', 'file', 'year')}),
        ("Visibility", {'fields': ('is_published', 'is_featured', 'published_at')}),
        ("Stats", {'fields': ('download_count',), 'classes': ('collapse',)}),
        ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📎 Open</a>', obj.file.url)
        return '—'
    file_link.short_description = 'File'

    def file_link_detail(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank" class="button">📎 Open Document</a>', obj.file.url)
        return '(no file uploaded)'
    file_link_detail.short_description = 'Current File'
