from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventSpeaker


class EventSpeakerInline(admin.TabularInline):
    model = EventSpeaker
    extra = 1
    fields = ('name', 'role', 'bio', 'photo', 'order')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('cover_thumb', 'title', 'event_type', 'location', 'start_datetime', 'is_published')
    list_filter = ('is_published', 'event_type')
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'cover_preview')
    date_hierarchy = 'start_datetime'
    inlines = [EventSpeakerInline]
    save_on_top = True
    fieldsets = (
        ("Event Info", {'fields': ('title', 'slug', 'event_type', 'description')}),
        ("Cover Image", {'fields': ('cover_preview', 'cover_image')}),
        ("Schedule & Location", {'fields': ('start_datetime', 'end_datetime', 'location', 'location_detail', 'registration_link')}),
        ("Visibility", {'fields': ('is_published',)}),
        ("SEO", {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width:56px;height:36px;border-radius:4px;object-fit:cover">', obj.cover_image.url)
        return '📅'
    cover_thumb.short_description = ''

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px">', obj.cover_image.url)
        return '(no cover image)'
    cover_preview.short_description = 'Current Cover'
