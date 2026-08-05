from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'subject', 'colored_status', 'created_at', 'reply_link')
    list_filter = ('is_resolved', 'department', 'created_at')
    # Note: is_resolved shown via colored_status method — use inline edit on detail page
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'reply_link')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    save_on_top = True
    fieldsets = (
        ('Inquiry', {'fields': ('name', 'email', 'phone', 'department', 'subject', 'message')}),
        ('Admin Notes', {'fields': ('is_resolved', 'admin_notes', 'reply_link')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def colored_status(self, obj):
        if obj.is_resolved:
            return format_html('<span style="color:#16a34a;font-weight:600">✅ Resolved</span>')
        return format_html('<span style="color:#d97706;font-weight:600">⏳ Pending</span>')
    colored_status.short_description = 'Status'

    def reply_link(self, obj):
        if obj.email:
            subject = f"Re: {obj.subject}"
            return format_html(
                '<a href="mailto:{}?subject={}" class="button">📧 Reply by Email</a>',
                obj.email, subject
            )
        return '—'
    reply_link.short_description = 'Reply'
