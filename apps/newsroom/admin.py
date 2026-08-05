"""
apps/newsroom/admin.py — Enhanced with image previews.
NOTE: fieldset names use plain strings (no gettext_lazy + emoji) for
Python 3.14 + Django 5.0 compatibility.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import NewsCategory, NewsPost, NewsPostImage, PressRelease, LetterStatement, MediaAsset


class NewsPostImageInline(admin.TabularInline):
    model = NewsPostImage
    extra = 3
    fields = ('image', 'caption', 'order')
    verbose_name = "Additional Image"
    verbose_name_plural = "Additional Images (Gallery)"



@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('color_swatch', 'name', 'slug', 'color', 'order')
    list_editable = ('order', 'color')
    prepopulated_fields = {'slug': ('name',)}

    def color_swatch(self, obj):
        return format_html(
            '<div style="width:20px;height:20px;border-radius:4px;background:{};border:1px solid #e5e7eb"></div>',
            obj.color or '#ccc'
        )
    color_swatch.short_description = ''


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('cover_thumb', 'title', 'category', 'is_published', 'is_featured', 'published_at', 'author')
    list_filter = ('is_published', 'is_featured', 'category', 'published_at')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'summary', 'body', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'cover_preview')
    date_hierarchy = 'published_at'
    save_on_top = True
    inlines = [NewsPostImageInline]
    fieldsets = (
        ("Content", {'fields': ('title', 'slug', 'category', 'author', 'summary', 'body')}),
        ("Cover Image", {'fields': ('cover_preview', 'cover_image')}),
        ("Publication", {'fields': ('is_published', 'is_featured', 'published_at')}),
        ("SEO", {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
        ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:56px;height:36px;border-radius:4px;object-fit:cover">', obj.cover_image.url)
        return '—'
    cover_thumb.short_description = ''

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px">', obj.cover_image.url)
        return '(no image yet — save first, then upload)'
    cover_preview.short_description = 'Current Image'

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('cover_thumb', 'title', 'is_published', 'published_at', 'has_attachment')
    list_filter = ('is_published', 'published_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'cover_preview', 'attachment_link')
    date_hierarchy = 'published_at'
    save_on_top = True
    fieldsets = (
        ("Content", {'fields': ('title', 'slug', 'summary', 'body')}),
        ("Cover Image", {'fields': ('cover_preview', 'cover_image')}),
        ("Attachment", {'fields': ('attachment_link', 'attachment')}),
        ("Publication", {'fields': ('is_published', 'published_at')}),
        ("SEO", {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:56px;height:36px;border-radius:4px;object-fit:cover">', obj.cover_image.url)
        return '—'
    cover_thumb.short_description = ''

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px">', obj.cover_image.url)
        return '(no image yet)'
    cover_preview.short_description = 'Current Cover'

    def attachment_link(self, obj):
        if obj.attachment:
            return format_html('<a href="{}" target="_blank" class="button">View Attachment</a>', obj.attachment.url)
        return '(no attachment)'
    attachment_link.short_description = 'Current Attachment'

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'PDF'


@admin.register(LetterStatement)
class LetterStatementAdmin(admin.ModelAdmin):
    list_display = ('title', 'addressed_to', 'date_issued', 'is_published')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title', 'addressed_to', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_issued'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Content", {'fields': ('title', 'slug', 'addressed_to', 'date_issued', 'body')}),
        ("Publication", {'fields': ('is_published',)}),
        ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'title', 'category', 'is_published', 'upload_date', 'order')
    list_filter = ('is_published', 'category')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'caption')
    readonly_fields = ('image_preview',)
    save_on_top = True
    fieldsets = (
        ("Media", {'fields': ('title', 'caption', 'image_preview', 'image', 'video_url', 'category')}),
        ("Publication", {'fields': ('is_published', 'order')}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly.append('upload_date')
        return readonly

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if obj is not None:
            fieldsets.append(("Timestamps", {'fields': ('upload_date',), 'classes': ('collapse',)}))
        return fieldsets

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:56px;height:36px;border-radius:4px;object-fit:cover">', obj.image.url)
        return '—'
    image_thumb.short_description = ''

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px">', obj.image.url)
        return '(no image yet)'
    image_preview.short_description = 'Current Image'
