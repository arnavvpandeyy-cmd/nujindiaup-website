"""
apps/membership/views.py — Full membership + member portal views
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from .models import MembershipApplication, MemberProfile
from .forms import MembershipApplicationForm, ApplicationStatusForm

logger = logging.getLogger('apps.membership')

# ──────────────────────────────────────────────────────────
# PUBLIC PAGES
# ──────────────────────────────────────────────────────────

def membership_info(request):
    """Membership information page."""
    return render(request, 'membership/info.html', {
        'breadcrumbs': [('Membership', None)],
        'page_title': 'Membership — NUJ UP',
    })


def public_member_grid(request):
    """
    Public directory / grid of active approved members.
    Only profiles with is_active_member=True (approved status) are displayed.
    """
    q = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '')
    type_filter = request.GET.get('type', '')

    members = MemberProfile.objects.select_related('user', 'application').filter(is_active_member=True).order_by('-created_at')

    if q:
        members = members.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(designation__icontains=q) |
            Q(organization__icontains=q) |
            Q(member_id__icontains=q)
        )
    if city_filter:
        members = members.filter(city=city_filter)
    if type_filter:
        members = members.filter(membership_type=type_filter)

    from apps.people.models import INDIAN_STATES
    paginator = Paginator(members, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'membership/member_grid.html', {
        'members': page_obj,
        'page_obj': page_obj,
        'cities': INDIAN_STATES,
        'membership_types': MembershipApplication.MEMBERSHIP_TYPES,
        'query': q,
        'selected_city': city_filter,
        'selected_type': type_filter,
        'total_count': members.count(),
        'breadcrumbs': [('Membership', '/membership/'), ('Member Directory', None)],
        'page_title': 'Member Directory — NUJ UP',
    })


def membership_apply(request):
    """Membership application form."""
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = 'submitted'
            application.submitted_at = timezone.now()
            application.save()

            try:
                send_mail(
                    subject=f"Membership Application Received — {application.reference_number}",
                    message=f"""Dear {application.full_name},

Thank you for applying for membership with the National Union of Journalists (Uttar Pradesh).

Your application reference number is: {application.reference_number}

You can track your application status at:
{getattr(settings, 'SITE_URL', 'http://localhost:8000')}/membership/status/

Our membership committee will review your application and contact you shortly.

Regards,
NUJ UP Membership Committee
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[application.email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Failed to send membership email: {e}")

            return redirect('membership:success', ref=application.reference_number)
    else:
        form = MembershipApplicationForm()

    return render(request, 'membership/apply.html', {
        'form': form,
        'breadcrumbs': [('Membership', '/membership/'), ('Apply', None)],
        'page_title': 'Apply for Membership',
    })


def membership_success(request, ref):
    return render(request, 'membership/success.html', {
        'reference_number': ref,
        'breadcrumbs': [('Membership', '/membership/'), ('Application Submitted', None)],
        'page_title': 'Application Submitted',
    })


def membership_status(request):
    """Check application status by reference + email."""
    form = ApplicationStatusForm()
    application = None
    searched = False

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            searched = True
            ref = form.cleaned_data['reference_number'].upper().strip()
            email = form.cleaned_data['email'].lower().strip()
            try:
                application = MembershipApplication.objects.get(
                    reference_number=ref, email__iexact=email,
                )
            except MembershipApplication.DoesNotExist:
                messages.error(request, "No application found. Please check your reference number and email.")

    return render(request, 'membership/status.html', {
        'form': form,
        'application': application,
        'searched': searched,
        'breadcrumbs': [('Membership', '/membership/'), ('Check Status', None)],
        'page_title': 'Check Application Status',
    })


# ──────────────────────────────────────────────────────────
# MEMBER PORTAL — AUTH
# ──────────────────────────────────────────────────────────

def member_login(request):
    """Member portal login page — routes by role after authentication."""
    if request.user.is_authenticated:
        return _role_redirect(request.user, request)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return _role_redirect(user, request)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'membership/login.html', {
        'page_title': 'Member Login — NUJ UP',
        'next': request.GET.get('next', ''),
    })


def _role_redirect(user, request):
    """Redirect user to the correct dashboard based on their role."""
    if user.is_superuser or user.is_staff:
        return redirect('/portal/admin-panel/')
    try:
        role = user.member_profile.role
        if role == 'super_admin':
            return redirect('/portal/admin-panel/')
        elif role == 'city_admin':
            return redirect('/portal/city-admin/')
    except Exception:
        pass
    return redirect('membership:dashboard')



def member_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('membership:login')


# ──────────────────────────────────────────────────────────
# MEMBER PORTAL — DASHBOARD (login required)
# ──────────────────────────────────────────────────────────

@login_required(login_url='/membership/login/')
def member_dashboard(request):
    """Member portal main dashboard."""
    try:
        profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        messages.error(request, "No member profile found for your account.")
        return redirect('membership:login')

    return render(request, 'membership/dashboard.html', {
        'profile': profile,
        'page_title': f'Dashboard — {profile.get_full_name()}',
    })


@login_required(login_url='/membership/login/')
def member_profile_edit(request):
    """Edit member profile."""
    try:
        profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        return redirect('membership:login')

    if request.method == 'POST':
        # Update allowed fields only
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        profile.phone = request.POST.get('phone', profile.phone)
        profile.designation = request.POST.get('designation', profile.designation)
        profile.organization = request.POST.get('organization', profile.organization)
        profile.address = request.POST.get('address', profile.address)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.city = request.POST.get('city', profile.city)

        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        if 'press_card' in request.FILES:
            profile.press_card = request.FILES['press_card']

        profile.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('membership:dashboard')

    from apps.people.models import INDIAN_STATES
    return render(request, 'membership/profile_edit.html', {
        'profile': profile,
        'cities': INDIAN_STATES,
        'page_title': 'Edit Profile',
    })


@login_required(login_url='/membership/login/')
def member_card(request):
    """Printable digital membership card."""
    try:
        profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        return redirect('membership:login')

    return render(request, 'membership/member_card.html', {
        'profile': profile,
        'page_title': 'My Membership Card',
    })


@login_required(login_url='/membership/login/')
def change_password(request):
    """Change member password."""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
        elif len(new_password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect('membership:login')

    return render(request, 'membership/change_password.html', {
        'page_title': 'Change Password',
    })
