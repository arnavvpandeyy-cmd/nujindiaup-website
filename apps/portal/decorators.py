"""
apps/portal/decorators.py — Role-based access decorators for the portal system.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def super_admin_required(view_func):
    """Only super_admin role (or Django staff/superuser) can access."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/membership/login/?next=' + request.path)
        # Django superuser always gets access
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        # Check portal role
        try:
            if request.user.member_profile.role == 'super_admin':
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        messages.error(request, "You do not have Super Admin access.")
        return redirect('/membership/portal/')
    return _wrapped


def city_admin_required(view_func):
    """city_admin, super_admin, or Django staff can access."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/membership/login/?next=' + request.path)
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        try:
            role = request.user.member_profile.role
            if role in ('city_admin', 'super_admin'):
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        messages.error(request, "You do not have City Admin access.")
        return redirect('/membership/portal/')
    return _wrapped


def portal_login_required(view_func):
    """Any authenticated user with a member profile."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/membership/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return _wrapped
