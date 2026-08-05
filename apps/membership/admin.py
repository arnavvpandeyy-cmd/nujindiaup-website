"""
apps/membership/admin.py — Enhanced with photo previews, approval workflow, MemberProfile management
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import MembershipApplication, MemberProfile


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number', 'full_name', 'email', 'state',
        'membership_type', 'colored_status', 'photo_thumb', 'submitted_at',
    )
    list_filter = ('status', 'membership_type', 'state', 'created_at')
    search_fields = ('reference_number', 'full_name', 'email', 'organization', 'phone')
    readonly_fields = (
        'reference_number', 'submitted_at', 'created_at', 'updated_at',
        'photo_preview', 'id_proof_link', 'press_card_link',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        (_("📋 Reference & Status"), {
            'fields': ('reference_number', 'status', 'admin_notes'),
        }),
        (_("👤 Personal Details"), {
            'fields': ('full_name', 'email', 'phone', 'dob', 'address', 'state', 'pincode')
        }),
        (_("💼 Professional Details"), {
            'fields': ('designation', 'organization', 'experience_years', 'membership_type')
        }),
        (_("📄 Documents"), {
            'fields': ('photo_preview', 'photo', 'id_proof_link', 'id_proof', 'press_card_link', 'press_card')
        }),
        (_("🕒 Timestamps"), {
            'fields': ('submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_under_review', 'mark_approved', 'mark_rejected', 'mark_needs_clarification', 'create_member_accounts']

    def colored_status(self, obj):
        colors = {
            'draft':               ('#6b7280', '⚪ Draft'),
            'submitted':           ('#2563eb', '🔵 Submitted'),
            'under_review':        ('#d97706', '🟡 Under Review'),
            'approved':            ('#16a34a', '🟢 Approved'),
            'rejected':            ('#dc2626', '🔴 Rejected'),
            'needs_clarification': ('#ea580c', '🟠 Needs Clarification'),
        }
        color, label = colors.get(obj.status, ('#6b7280', obj.status))
        return format_html('<span style="color:{};font-weight:600">{}</span>', color, label)
    colored_status.short_description = 'Status'

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #e5e7eb">', obj.photo.url)
        return '—'
    photo_thumb.short_description = 'Photo'

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px;box-shadow:0 1px 4px rgba(0,0,0,.2)">', obj.photo.url)
        return '(no photo uploaded)'
    photo_preview.short_description = 'Photo Preview'

    def id_proof_link(self, obj):
        if obj.id_proof:
            return format_html('<a href="{}" target="_blank" class="button">📎 Open ID Proof</a>', obj.id_proof.url)
        return '(not uploaded)'
    id_proof_link.short_description = 'ID Proof File'

    def press_card_link(self, obj):
        if obj.press_card:
            return format_html('<a href="{}" target="_blank" class="button">📎 Open Press Card</a>', obj.press_card.url)
        return '(not uploaded)'
    press_card_link.short_description = 'Press Card File'

    def mark_under_review(self, request, queryset):
        queryset.update(status='under_review')
        self.message_user(request, f"{queryset.count()} application(s) marked as Under Review.")
    mark_under_review.short_description = "🟡 Mark → Under Review"

    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} application(s) Approved.")
    mark_approved.short_description = "🟢 Mark → Approved"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} application(s) Rejected.")
    mark_rejected.short_description = "🔴 Mark → Rejected"

    def mark_needs_clarification(self, request, queryset):
        queryset.update(status='needs_clarification')
        self.message_user(request, f"{queryset.count()} application(s) flagged.")
    mark_needs_clarification.short_description = "🟠 Mark → Needs Clarification"

    def create_member_accounts(self, request, queryset):
        """Create User + MemberProfile for approved applications that don't have one yet."""
        created = 0
        skipped = 0
        for app in queryset.filter(status='approved'):
            if hasattr(app, 'member_profile'):
                skipped += 1
                continue
            # Create or get user
            username = app.email.split('@')[0].lower().replace('.', '_')
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            import secrets
            temp_password = secrets.token_urlsafe(10)
            user = User.objects.create_user(
                username=username,
                email=app.email,
                password=temp_password,
                first_name=app.full_name.split()[0] if app.full_name else '',
                last_name=' '.join(app.full_name.split()[1:]) if len(app.full_name.split()) > 1 else '',
            )
            MemberProfile.objects.create(
                user=user,
                application=app,
                membership_type=app.membership_type,
                city=app.state,
                designation=app.designation,
                organization=app.organization,
                phone=app.phone,
                address=app.address,
                photo=app.photo if app.photo else None,
                press_card=app.press_card if app.press_card else None,
            )
            created += 1
        self.message_user(request, f"✅ Created {created} member account(s). {skipped} skipped (already had accounts).")
    create_member_accounts.short_description = "✅ Create member login accounts for approved"


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'member_id', 'get_full_name', 'get_email', 'city', 'membership_type', 'is_active_member', 'membership_valid_until')
    list_filter = ('is_active_member', 'membership_type', 'city')
    search_fields = ('member_id', 'user__first_name', 'user__last_name', 'user__email', 'organization', 'designation')
    readonly_fields = ('member_id', 'created_at', 'updated_at', 'photo_preview', 'press_card_link')
    list_editable = ('is_active_member', 'membership_valid_until')
    save_on_top = True
    raw_id_fields = ('user', 'application')

    fieldsets = (
        (_("🪪 Member ID"), {'fields': ('member_id', 'user', 'application')}),
        (_("📸 Photo"), {'fields': ('photo_preview', 'photo')}),
        (_("💼 Professional"), {'fields': ('membership_type', 'city', 'designation', 'organization', 'phone', 'address', 'bio')}),
        (_("📄 Documents"), {'fields': ('press_card_link', 'press_card')}),
        (_("📋 Status"), {'fields': ('is_active_member', 'membership_valid_until')}),
        (_("🕒 Timestamps"), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #e5e7eb">', obj.photo.url)
        return '👤'
    photo_thumb.short_description = ''

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;margin-top:8px">', obj.photo.url)
        return '(no photo)'
    photo_preview.short_description = 'Current Photo'

    def press_card_link(self, obj):
        if obj.press_card:
            return format_html('<a href="{}" target="_blank" class="button">📎 Open Press Card</a>', obj.press_card.url)
        return '(not uploaded)'
    press_card_link.short_description = 'Press Card'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
