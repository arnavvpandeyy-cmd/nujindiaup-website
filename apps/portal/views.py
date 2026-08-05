"""
apps/portal/views.py — Super Admin Dashboard + City Admin + Member Portal views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .decorators import super_admin_required, city_admin_required, portal_login_required
from apps.membership.models import MemberProfile, MembershipApplication
from apps.people.models import OfficeBearer, StateUnit, StateUnitMember, INDIAN_STATES
from apps.newsroom.models import NewsPost, PressRelease, LetterStatement, MediaAsset, NewsCategory
from apps.events.models import Event
from apps.documents.models import Document
from apps.contact.models import ContactInquiry
from apps.pages.models import HomeSlide
from apps.core.models import SiteSettings, Announcement


# ──────────────────────────────────────────────────────────
# CUSTOM ADMIN PANEL DASHBOARD
# ──────────────────────────────────────────────────────────

@super_admin_required
def admin_panel(request):
    """Full-featured custom admin dashboard with all modules and recent actions."""
    from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
    from django.contrib.auth.models import User as AuthUser

    recent_actions = LogEntry.objects.select_related(
        'user', 'content_type'
    ).order_by('-action_time')[:20]

    ctx = {
        'recent_actions': recent_actions,
        'ADDITION': ADDITION,
        'CHANGE': CHANGE,
        'DELETION': DELETION,
        'counts': {
            'users': AuthUser.objects.count(),
            'members': MemberProfile.objects.count(),
            'applications': MembershipApplication.objects.filter(status__in=['submitted', 'under_review']).count(),
            'news': NewsPost.objects.count(),
            'press_releases': PressRelease.objects.count(),
            'letters': LetterStatement.objects.count(),
            'media': MediaAsset.objects.count(),
            'events': Event.objects.count(),
            'documents': Document.objects.count(),
            'city_units': StateUnit.objects.count(),
            'office_bearers': OfficeBearer.objects.count(),
            'contact': ContactInquiry.objects.count(),
        },
        'page_title': 'NUJ UP — Site Administration',
    }
    return render(request, 'portal/admin_panel.html', ctx)


# ──────────────────────────────────────────────────────────

@super_admin_required
def super_admin_home(request):
    """Super Admin dashboard home — overview stats."""
    now = timezone.now()
    pending_count = MembershipApplication.objects.filter(
        status__in=['submitted', 'under_review']).count()
    ctx = {
        'total_members': MemberProfile.objects.filter(is_active_member=True).count(),
        'pending_applications': pending_count,
        'pending_count': pending_count,
        'total_city_units': StateUnit.objects.filter(is_published=True).count(),
        'total_news': NewsPost.objects.filter(is_published=True).count(),
        'total_bearers': OfficeBearer.objects.filter(is_published=True).count(),
        'recent_applications': MembershipApplication.objects.filter(
            status__in=['submitted', 'under_review']).order_by('-submitted_at')[:5],
        'recent_members': MemberProfile.objects.select_related('user').order_by('-created_at')[:5],
        'quick_actions': [
            ('Add News', '/portal/admin/news/add/', '📰'),
            ('Add Press Release', '/portal/admin/press-release/add/', '📜'),
            ('Add Office Bearer', '/portal/admin/office-bearers/add/', '👤'),
            ('Add City Unit', '/portal/admin/city-units/add/', '🏙️'),
            ('Review Applications', '/portal/admin/applications/', '✅'),
            ('Django Admin', '/nuj-admin/', '⚙️'),
        ],
        'page_title': 'Super Admin Dashboard',
        'active_tab': 'home',
    }
    return render(request, 'portal/admin_home.html', ctx)


@super_admin_required
def admin_members(request):
    """Manage all members — list, search, filter, set roles."""
    q = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '')
    role_filter = request.GET.get('role', '')

    profiles = MemberProfile.objects.select_related('user', 'application').order_by('-created_at')
    if q:
        profiles = profiles.filter(
            Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) |
            Q(user__email__icontains=q) | Q(member_id__icontains=q) |
            Q(organization__icontains=q)
        )
    if city_filter:
        profiles = profiles.filter(city=city_filter)
    if role_filter:
        profiles = profiles.filter(role=role_filter)

    return render(request, 'portal/admin_members.html', {
        'profiles': profiles,
        'cities': INDIAN_STATES,
        'roles': MemberProfile.ROLE_CHOICES,
        'q': q, 'city_filter': city_filter, 'role_filter': role_filter,
        'page_title': 'Manage Members',
        'active_tab': 'members',
    })


@super_admin_required
def admin_member_edit(request, pk):
    """Edit a member's role, city, profile details."""
    profile = get_object_or_404(MemberProfile, pk=pk)
    if request.method == 'POST':
        # Update role
        profile.role = request.POST.get('role', 'member')
        profile.managed_city = request.POST.get('managed_city', '')
        profile.is_active_member = request.POST.get('is_active_member') == 'on'
        profile.membership_valid_until = request.POST.get('membership_valid_until') or None
        profile.designation = request.POST.get('designation', profile.designation)
        profile.organization = request.POST.get('organization', profile.organization)
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()
        # Update user
        user = profile.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, f"Member '{profile.get_full_name()}' updated.")
        return redirect('portal:admin_members')

    return render(request, 'portal/admin_member_edit.html', {
        'profile': profile,
        'cities': INDIAN_STATES,
        'roles': MemberProfile.ROLE_CHOICES,
        'page_title': f'Edit Member — {profile.get_full_name()}',
        'active_tab': 'members',
    })


@super_admin_required
def admin_applications(request):
    """Review membership applications — approve/reject."""
    status_filter = request.GET.get('status', 'submitted')
    apps = MembershipApplication.objects.order_by('-submitted_at')
    if status_filter:
        apps = apps.filter(status=status_filter)

    return render(request, 'portal/admin_applications.html', {
        'applications': apps,
        'status_filter': status_filter,
        'status_choices': MembershipApplication.STATUS_CHOICES,
        'page_title': 'Membership Applications',
        'active_tab': 'applications',
    })


@super_admin_required
def admin_application_detail(request, pk):
    """View and action on a single membership application."""
    app = get_object_or_404(MembershipApplication, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        app.admin_notes = request.POST.get('admin_notes', app.admin_notes)

        if action == 'approve':
            app.status = 'approved'
            app.save()
            # Create member login if not already done
            _create_member_login(app)
            messages.success(request, f"Application approved. Login account created for {app.full_name}.")
        elif action == 'reject':
            app.status = 'rejected'
            app.save()
            messages.warning(request, f"Application rejected for {app.full_name}.")
        elif action == 'review':
            app.status = 'under_review'
            app.save()
            messages.info(request, "Application marked as Under Review.")
        elif action == 'clarify':
            app.status = 'needs_clarification'
            app.save()
            messages.info(request, "Application marked as Needs Clarification.")
        else:
            app.save()
            messages.success(request, "Notes saved.")
        return redirect('portal:admin_application_detail', pk=pk)

    return render(request, 'portal/admin_application_detail.html', {
        'app': app,
        'page_title': f'Application — {app.full_name}',
        'active_tab': 'applications',
    })


def _create_member_login(application):
    """Helper: create a User + MemberProfile for an approved application."""
    if hasattr(application, 'member_profile') and application.member_profile:
        return  # Already exists
    base_username = application.email.split('@')[0].lower().replace('.', '_')
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    import secrets
    temp_password = secrets.token_urlsafe(10)
    user = User.objects.create_user(
        username=username,
        email=application.email,
        first_name=application.full_name.split()[0],
        last_name=' '.join(application.full_name.split()[1:]),
        password=temp_password,
    )
    MemberProfile.objects.create(
        user=user,
        application=application,
        membership_type=application.membership_type,
        city=application.state,
        designation=application.designation,
        organization=application.organization,
        phone=application.phone,
        address=application.address,
        photo=application.photo,
        press_card=application.press_card,
    )
    return username, temp_password


@super_admin_required
def admin_city_units(request):
    """Manage all city units."""
    q = request.GET.get('q', '').strip()
    units = StateUnit.objects.order_by('name')
    if q:
        units = units.filter(Q(name__icontains=q) | Q(state__icontains=q))

    return render(request, 'portal/admin_city_units.html', {
        'units': units,
        'q': q,
        'page_title': 'City Units',
        'active_tab': 'city_units',
    })


@super_admin_required
def admin_city_unit_edit(request, pk=None):
    """Add or edit a city unit with its position holders."""
    unit = get_object_or_404(StateUnit, pk=pk) if pk else None

    if request.method == 'POST':
        # Handle basic unit fields
        if not unit:
            unit = StateUnit()
        unit.name = request.POST.get('name', unit.name if unit.pk else '')
        unit.state = request.POST.get('state', '')
        unit.established_year = request.POST.get('established_year') or None
        unit.member_count = request.POST.get('member_count') or None
        unit.phone = request.POST.get('phone', '')
        unit.email = request.POST.get('email', '')
        unit.address = request.POST.get('address', '')
        unit.website = request.POST.get('website', '')
        unit.description = request.POST.get('description', '')
        unit.is_published = request.POST.get('is_published') == 'on'
        if 'cover_image' in request.FILES:
            unit.cover_image = request.FILES['cover_image']
        if not unit.slug:
            from django.utils.text import slugify
            unit.slug = slugify(unit.name)
        unit.save()

        # Handle position holders — clear and rebuild
        unit.members.all().delete()
        roles = request.POST.getlist('member_role')
        names = request.POST.getlist('member_name')
        phones = request.POST.getlist('member_phone')
        emails = request.POST.getlist('member_email')
        for i, name in enumerate(names):
            if name.strip():
                m = StateUnitMember(
                    state_unit=unit,
                    name=name.strip(),
                    role=roles[i] if i < len(roles) else '',
                    phone=phones[i] if i < len(phones) else '',
                    email=emails[i] if i < len(emails) else '',
                    order=i,
                )
                photo_key = f'member_photo_{i}'
                if photo_key in request.FILES:
                    m.photo = request.FILES[photo_key]
                m.save()

        messages.success(request, f"City Unit '{unit.name}' saved successfully.")
        return redirect('portal:admin_city_units')

    members = list(unit.members.all()) if unit else []
    return render(request, 'portal/admin_city_unit_edit.html', {
        'unit': unit,
        'members': members,
        'cities': INDIAN_STATES,
        'page_title': f'Edit City Unit — {unit.name}' if unit else 'Add City Unit',
        'active_tab': 'city_units',
    })


@super_admin_required
def admin_office_bearers(request):
    """Manage UP-level office bearers."""
    bearers = OfficeBearer.objects.order_by('category', 'order')
    return render(request, 'portal/admin_office_bearers.html', {
        'bearers': bearers,
        'page_title': 'UP Office Bearers',
        'active_tab': 'bearers',
    })


@super_admin_required
def admin_bearer_edit(request, pk=None):
    """Add or edit an office bearer with photo upload."""
    bearer = get_object_or_404(OfficeBearer, pk=pk) if pk else None

    if request.method == 'POST':
        if not bearer:
            bearer = OfficeBearer()
        bearer.name = request.POST.get('name', '')
        bearer.role = request.POST.get('role', '')
        bearer.category = request.POST.get('category', 'executive_member')
        bearer.state = request.POST.get('state', '')
        bearer.bio = request.POST.get('bio', '')
        bearer.email = request.POST.get('email', '')
        bearer.phone = request.POST.get('phone', '')
        bearer.show_contact = request.POST.get('show_contact') == 'on'
        bearer.is_featured = request.POST.get('is_featured') == 'on'
        bearer.is_published = request.POST.get('is_published') == 'on'
        bearer.order = int(request.POST.get('order', 0) or 0)
        bearer.term_start = request.POST.get('term_start') or None
        bearer.term_end = request.POST.get('term_end') or None
        if 'photo' in request.FILES:
            bearer.photo = request.FILES['photo']
        if not bearer.slug:
            from django.utils.text import slugify
            bearer.slug = slugify(bearer.name)
        bearer.save()
        messages.success(request, f"Office bearer '{bearer.name}' saved.")
        return redirect('portal:admin_office_bearers')

    return render(request, 'portal/admin_bearer_edit.html', {
        'bearer': bearer,
        'categories': OfficeBearer.CATEGORY_CHOICES,
        'cities': INDIAN_STATES,
        'page_title': f'Edit Bearer — {bearer.name}' if bearer else 'Add Office Bearer',
        'active_tab': 'bearers',
    })


@super_admin_required
def admin_news(request):
    """Manage news posts and press releases."""
    news = NewsPost.objects.order_by('-published_at')[:30]
    releases = PressRelease.objects.order_by('-published_at')[:20]
    return render(request, 'portal/admin_news.html', {
        'news': news,
        'releases': releases,
        'page_title': 'News & Press Releases',
        'active_tab': 'news',
    })


@super_admin_required
def admin_news_edit(request, pk=None):
    """Add or edit a news post."""
    post = get_object_or_404(NewsPost, pk=pk) if pk else None

    if request.method == 'POST':
        from apps.newsroom.models import NewsCategory
        if not post:
            post = NewsPost()
        post.title = request.POST.get('title', '')
        post.summary = request.POST.get('summary', '')
        post.body = request.POST.get('body', '')
        post.author = request.POST.get('author', '') or (request.user.get_full_name() or request.user.username)
        cat_id = request.POST.get('category')
        if cat_id:
            try:
                post.category = NewsCategory.objects.get(pk=cat_id)
            except NewsCategory.DoesNotExist:
                pass
        post.is_published = request.POST.get('is_published') == 'on'
        post.is_featured = request.POST.get('is_featured') == 'on'
        published_at = request.POST.get('published_at')
        if published_at:
            from django.utils.dateparse import parse_datetime
            post.published_at = parse_datetime(published_at) or timezone.now()
        else:
            post.published_at = timezone.now()
        if 'cover_image' in request.FILES:
            post.cover_image = request.FILES['cover_image']
        if not post.slug:
            from django.utils.text import slugify
            post.slug = slugify(post.title)
        post.save()

        # ── Gallery images: handle new uploads, deletes, caption updates ──
        from apps.newsroom.models import NewsPostImage
        # New uploads
        i = 0
        while True:
            key = f'gallery_image_new_{i}'
            if key not in request.FILES:
                if i > 20:
                    break
                i += 1
                continue
            caption = request.POST.get(f'gallery_caption_new_{i}', '')
            NewsPostImage.objects.create(post=post, image=request.FILES[key], caption=caption, order=i)
            i += 1
        # Delete marked
        for img in post.extra_images.all():
            if request.POST.get(f'gallery_delete_{img.pk}'):
                img.delete()
            else:
                caption = request.POST.get(f'gallery_caption_{img.pk}', img.caption)
                if caption != img.caption:
                    img.caption = caption
                    img.save(update_fields=['caption'])

        messages.success(request, f"News post '{post.title}' saved.")
        return redirect('portal:admin_news')


    from apps.newsroom.models import NewsCategory
    return render(request, 'portal/admin_news_edit.html', {
        'post': post,
        'categories': NewsCategory.objects.all(),
        'page_title': f'Edit News — {post.title}' if post else 'Add News Post',
        'active_tab': 'news',
    })


@super_admin_required
def admin_press_release_edit(request, pk=None):
    """Add or edit a press release."""
    release = get_object_or_404(PressRelease, pk=pk) if pk else None

    if request.method == 'POST':
        if not release:
            release = PressRelease()
        release.title = request.POST.get('title', '')
        release.summary = request.POST.get('summary', '')
        release.body = request.POST.get('body', '')
        release.is_published = request.POST.get('is_published') == 'on'
        published_at = request.POST.get('published_at')
        if published_at:
            from django.utils.dateparse import parse_datetime
            release.published_at = parse_datetime(published_at) or timezone.now()
        else:
            release.published_at = timezone.now()
        if 'cover_image' in request.FILES:
            release.cover_image = request.FILES['cover_image']
        if 'attachment' in request.FILES:
            release.attachment = request.FILES['attachment']
        if not release.slug:
            from django.utils.text import slugify
            release.slug = slugify(release.title)
        release.save()
        messages.success(request, f"Press release '{release.title}' saved.")
        return redirect('portal:admin_news')

    return render(request, 'portal/admin_press_release_edit.html', {
        'release': release,
        'page_title': f'Edit Press Release — {release.title}' if release else 'Add Press Release',
        'active_tab': 'news',
    })


# ──────────────────────────────────────────────────────────
# CITY ADMIN DASHBOARD
# ──────────────────────────────────────────────────────────

@city_admin_required
def city_admin_home(request):
    """City Admin dashboard — manage own city unit."""
    try:
        profile = request.user.member_profile
        city_code = profile.managed_city or profile.city
    except Exception:
        city_code = ''

    unit = StateUnit.objects.filter(state=city_code).first() if city_code else None
    city_members = MemberProfile.objects.filter(city=city_code).select_related('user') if city_code else []
    city_apps = MembershipApplication.objects.filter(
        state=city_code, status__in=['submitted', 'under_review']) if city_code else []

    return render(request, 'portal/city_admin_home.html', {
        'unit': unit,
        'city_code': city_code,
        'city_name': dict(INDIAN_STATES).get(city_code, city_code),
        'city_members': city_members,
        'city_apps': city_apps,
        'page_title': 'City Admin Dashboard',
        'active_tab': 'city_home',
    })


@city_admin_required
def city_admin_unit_edit(request):
    """City admin edits their own city unit."""
    try:
        profile = request.user.member_profile
        city_code = profile.managed_city or profile.city
    except Exception:
        city_code = ''

    unit = StateUnit.objects.filter(state=city_code).first()
    if not unit:
        messages.error(request, "No city unit found for your city. Ask the Super Admin to create it first.")
        return redirect('portal:city_admin_home')

    if request.method == 'POST':
        unit.phone = request.POST.get('phone', unit.phone)
        unit.email = request.POST.get('email', unit.email)
        unit.address = request.POST.get('address', unit.address)
        unit.website = request.POST.get('website', unit.website)
        unit.description = request.POST.get('description', unit.description)
        unit.member_count = request.POST.get('member_count') or unit.member_count
        if 'cover_image' in request.FILES:
            unit.cover_image = request.FILES['cover_image']
        unit.save()

        # Update position holders
        unit.members.all().delete()
        roles = request.POST.getlist('member_role')
        names = request.POST.getlist('member_name')
        phones = request.POST.getlist('member_phone')
        emails_list = request.POST.getlist('member_email')
        for i, name in enumerate(names):
            if name.strip():
                m = StateUnitMember(
                    state_unit=unit,
                    name=name.strip(),
                    role=roles[i] if i < len(roles) else '',
                    phone=phones[i] if i < len(phones) else '',
                    email=emails_list[i] if i < len(emails_list) else '',
                    order=i,
                )
                photo_key = f'member_photo_{i}'
                if photo_key in request.FILES:
                    m.photo = request.FILES[photo_key]
                m.save()

        messages.success(request, "City unit updated successfully.")
        return redirect('portal:city_admin_home')

    members = list(unit.members.all())
    return render(request, 'portal/city_admin_unit_edit.html', {
        'unit': unit,
        'members': members,
        'page_title': f'Edit {unit.name}',
        'active_tab': 'edit_unit',
    })


# ──────────────────────────────────────────────────────────
# ENHANCED MEMBER DASHBOARD — city-specific feed
# ──────────────────────────────────────────────────────────

@portal_login_required
def member_city_dashboard(request):
    """Enhanced member dashboard with city-specific content."""
    try:
        profile = request.user.member_profile
    except Exception:
        return redirect('/membership/login/')

    city_code = profile.city
    city_unit = StateUnit.objects.filter(state=city_code).first() if city_code else None
    city_bearers = StateUnitMember.objects.filter(
        state_unit=city_unit).order_by('order') if city_unit else []

    # Latest news (general)
    latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_at')[:4]
    # Upcoming events
    upcoming_events = Event.objects.filter(
        is_published=True, start_datetime__gte=timezone.now()
    ).order_by('start_datetime')[:3]
    # Recent press releases
    press_releases = PressRelease.objects.filter(is_published=True).order_by('-published_at')[:3]
    # Featured documents
    documents = Document.objects.filter(is_published=True, is_featured=True).order_by('-published_at')[:4]

    return render(request, 'portal/member_city_dashboard.html', {
        'profile': profile,
        'city_unit': city_unit,
        'city_name': dict(INDIAN_STATES).get(city_code, 'Your City') if city_code else 'Uttar Pradesh',
        'city_bearers': city_bearers,
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
        'press_releases': press_releases,
        'documents': documents,
        'page_title': f'My Dashboard — {profile.get_full_name()}',
    })


# ──────────────────────────────────────────────────────────
# ADDITIONAL PORTAL ADMIN MODULE VIEWS
# ──────────────────────────────────────────────────────────

@super_admin_required
def admin_contact(request):
    """Manage contact inquiries in custom portal theme."""
    inquiries = ContactInquiry.objects.order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter == 'resolved':
        inquiries = inquiries.filter(is_resolved=True)
    elif status_filter == 'pending':
        inquiries = inquiries.filter(is_resolved=False)

    if request.method == 'POST':
        inquiry_id = request.POST.get('inquiry_id')
        action = request.POST.get('action')
        if inquiry_id:
            inquiry = get_object_or_404(ContactInquiry, pk=inquiry_id)
            if action == 'toggle_resolve':
                inquiry.is_resolved = not inquiry.is_resolved
                inquiry.save()
                messages.success(request, f"Inquiry status updated for '{inquiry.name}'.")
            elif action == 'delete':
                inquiry.delete()
                messages.success(request, "Inquiry deleted.")
            return redirect('portal:admin_contact')

    return render(request, 'portal/admin_contact.html', {
        'inquiries': inquiries,
        'status_filter': status_filter,
        'page_title': 'Contact Inquiries — Portal Admin',
        'active_tab': 'contact',
    })


@super_admin_required
def admin_documents(request):
    """Manage documents and categories in custom portal theme."""
    docs = Document.objects.select_related('category').order_by('-published_at')
    return render(request, 'portal/admin_documents.html', {
        'documents': docs,
        'page_title': 'Manage Documents & Circulars',
        'active_tab': 'documents',
    })


@super_admin_required
def admin_events(request):
    """Manage events in custom portal theme."""
    events = Event.objects.order_by('-start_datetime')
    return render(request, 'portal/admin_events.html', {
        'events': events,
        'page_title': 'Manage Events',
        'active_tab': 'events',
    })


@super_admin_required
def admin_site_settings(request):
    """Manage site settings in custom portal theme."""
    settings_obj = SiteSettings.get()
    if request.method == 'POST':
        settings_obj.site_name = request.POST.get('site_name', settings_obj.site_name)
        settings_obj.tagline = request.POST.get('tagline', settings_obj.tagline)
        settings_obj.phone = request.POST.get('phone', settings_obj.phone)
        settings_obj.email = request.POST.get('email', settings_obj.email)
        settings_obj.office_address = request.POST.get('office_address', settings_obj.office_address)
        if 'logo' in request.FILES:
            settings_obj.logo = request.FILES['logo']
        settings_obj.save()
        messages.success(request, "Site settings updated successfully.")
        return redirect('portal:admin_site_settings')

    return render(request, 'portal/admin_site_settings.html', {
        'settings': settings_obj,
        'page_title': 'Site Settings — Portal Admin',
        'active_tab': 'site_settings',
    })


@super_admin_required
def admin_announcements(request):
    """Manage announcements in custom portal theme."""
    announcements = Announcement.objects.order_by('order', '-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            title = request.POST.get('title', '').strip()
            link = request.POST.get('link', '').strip()
            if title:
                Announcement.objects.create(title=title, link=link, is_published=True)
                messages.success(request, "Announcement added.")
        elif action == 'toggle':
            ann_id = request.POST.get('ann_id')
            ann = get_object_or_404(Announcement, pk=ann_id)
            ann.is_published = not ann.is_published
            ann.save()
            messages.success(request, "Announcement visibility toggled.")
        elif action == 'delete':
            ann_id = request.POST.get('ann_id')
            ann = get_object_or_404(Announcement, pk=ann_id)
            ann.delete()
            messages.success(request, "Announcement deleted.")
        return redirect('portal:admin_announcements')

    return render(request, 'portal/admin_announcements.html', {
        'announcements': announcements,
        'page_title': 'Manage Announcements',
        'active_tab': 'announcements',
    })


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


@super_admin_required
def admin_slides(request):
    """Manage Homepage Hero Slideshow Photos directly for Super Admin."""
    _ensure_homeslide_table()
    slides = HomeSlide.objects.order_by('order', '-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            title = request.POST.get('title', '').strip()
            link = request.POST.get('link', '').strip()
            order = request.POST.get('order', 0)
            if title and 'image' in request.FILES:
                HomeSlide.objects.create(
                    title=title,
                    image=request.FILES['image'],
                    link=link,
                    order=int(order) if order else 0,
                    is_published=True
                )
                messages.success(request, f"Hero slideshow photo '{title}' uploaded successfully.")
            else:
                messages.error(request, "Please provide both a title and an image file.")
        elif action == 'toggle':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(HomeSlide, pk=slide_id)
            slide.is_published = not slide.is_published
            slide.save()
            messages.success(request, f"Visibility updated for '{slide.title}'.")
        elif action == 'delete':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(HomeSlide, pk=slide_id)
            slide.delete()
            messages.success(request, "Slideshow photo deleted.")
        return redirect('portal:admin_slides')

    return render(request, 'portal/admin_slides.html', {
        'slides': slides,
        'page_title': 'Hero Slideshow Photos — Super Admin',
        'active_tab': 'hero_slides',
    })


