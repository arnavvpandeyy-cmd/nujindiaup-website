"""
apps/pages/admin.py
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import StaticPage, HomeSection, Testimonial, HomeSlide


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'is_published', 'updated_at')
    list_filter = ('is_published', 'key')
    search_fields = ('title', 'body')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('key', 'title', 'subtitle', 'body', 'cover_image', 'is_published', 'order')}),
        (_("SEO"), {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
        (_("Timestamps"), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        (None, {'fields': ('section_type', 'is_active', 'order')}),
        (_("Hero Content"), {
            'fields': ('hero_title', 'hero_subtitle', 'hero_cta_label', 'hero_cta_url',
                       'hero_secondary_cta_label', 'hero_secondary_cta_url', 'hero_image'),
            'classes': ('collapse',),
        }),
        (_("Leadership Message"), {
            'fields': ('message_author_name', 'message_author_role', 'message_author_photo',
                       'message_body', 'message_link'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('author_name', 'quote')


@admin.register(HomeSlide)
class HomeSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'order', 'created_at')
    list_editable = ('is_published', 'order')
    search_fields = ('title',)

