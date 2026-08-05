"""
apps/people/admin.py — Enhanced with photo previews and image display
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import OfficeBearer, StateUnit, StateUnitMember


class StateUnitMemberInline(admin.TabularInline):
    model = StateUnitMember
    extra = 1
    fields = ('name', 'role', 'phone', 'email', 'photo', 'order')
    readonly_fields = ('photo_thumb',)

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover">', obj.photo.url)
        return '—'
    photo_thumb.short_description = 'Photo'


@admin.register(OfficeBearer)
class OfficeBearerAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'name', 'role', 'category', 'state', 'is_national', 'is_featured', 'is_published', 'order')
    list_filter = ('is_published', 'is_national', 'is_featured', 'category', 'state')
    list_editable = ('is_published', 'is_national', 'is_featured', 'order')
    search_fields = ('name', 'role', 'bio', 'email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'photo_preview')
    save_on_top = True
    fieldsets = (
        ("Identity", {'fields': ('name', 'slug', 'role', 'category')}),
        ("Photo & Bio", {'fields': ('photo_preview', 'photo', 'bio')}),
        ("Location & Term", {'fields': ('state', 'zone', 'term_start', 'term_end')}),
        ("Contact", {'fields': ('email', 'phone', 'show_contact')}),
        ("Visibility", {'fields': ('is_featured', 'is_national', 'is_published', 'order')}),
        ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #e5e7eb">', obj.photo.url)
        return '👤'
    photo_thumb.short_description = ''

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px;box-shadow:0 2px 8px rgba(0,0,0,.15)">',
                obj.photo.url
            )
        return '(no photo — upload one above)'
    photo_preview.short_description = 'Current Photo'


@admin.register(StateUnit)
class StateUnitAdmin(admin.ModelAdmin):
    list_display = ('cover_thumb', 'name', 'state', 'established_year', 'member_count', 'is_published', 'order')
    list_filter = ('is_published', 'state')
    list_editable = ('is_published', 'order', 'member_count')
    search_fields = ('name', 'description', 'address', 'email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'cover_preview')
    inlines = [StateUnitMemberInline]
    save_on_top = True
    fieldsets = (
        ("Basic Info", {'fields': ('name', 'slug', 'state', 'established_year')}),
        ("Cover Image", {'fields': ('cover_preview', 'cover_image', 'description')}),
        ("Contact", {'fields': ('address', 'phone', 'email', 'website')}),
        ("Stats & Visibility", {'fields': ('member_count', 'is_published', 'order')}),
        ("Timestamps", {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:48px;height:32px;border-radius:4px;object-fit:cover">', obj.cover_image.url)
        return '🏙'
    cover_thumb.short_description = ''

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:160px;border-radius:8px;margin-top:8px">', obj.cover_image.url)
        return '(no cover image)'
    cover_preview.short_description = 'Current Cover'


@admin.register(StateUnitMember)
class StateUnitMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'name', 'role', 'state_unit', 'order')
    list_filter = ('state_unit',)
    search_fields = ('name', 'role', 'email')
    readonly_fields = ('photo_preview',)

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover">', obj.photo.url)
        return '👤'
    photo_thumb.short_description = ''

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:160px;border-radius:8px;margin-top:8px">', obj.photo.url)
        return '(no photo)'
    photo_preview.short_description = 'Photo Preview'
