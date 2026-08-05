"""
apps/membership/models.py — with MemberProfile for login portal
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimestampedModel
from apps.people.models import INDIAN_STATES


class MembershipApplication(TimestampedModel):
    """
    A membership application submitted by a journalist.
    Status lifecycle: draft → submitted → under_review → approved/rejected/needs_clarification
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_clarification', 'Needs Clarification'),
    ]

    MEMBERSHIP_TYPES = [
        ('ordinary', 'Ordinary Member'),
        ('associate', 'Associate Member'),
        ('honorary', 'Honorary Member'),
    ]

    # Reference number for tracking
    reference_number = models.CharField(
        max_length=20, unique=True, blank=True,
        verbose_name=_("Reference Number"),
        help_text=_("Auto-generated on submission.")
    )

    # Personal details
    full_name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    email = models.EmailField(verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    dob = models.DateField(verbose_name=_("Date of Birth"))
    address = models.TextField(verbose_name=_("Residential Address"))
    state = models.CharField(max_length=3, choices=INDIAN_STATES, verbose_name=_("City"))
    pincode = models.CharField(max_length=10, blank=True, verbose_name=_("PIN Code"))

    # Professional details
    designation = models.CharField(max_length=200, verbose_name=_("Current Designation"))
    organization = models.CharField(max_length=300, verbose_name=_("Current Organization / Publication"))
    experience_years = models.PositiveIntegerField(default=0, verbose_name=_("Years of Journalism Experience"))
    membership_type = models.CharField(
        max_length=20, choices=MEMBERSHIP_TYPES, default='ordinary',
        verbose_name=_("Membership Type")
    )

    # Documents
    id_proof = models.FileField(
        upload_to='membership/id_proofs/%Y/', blank=True, null=True,
        verbose_name=_("Identity Proof (PDF/JPG)"),
        help_text=_("Upload Aadhaar, PAN, Passport, or Voter ID.")
    )
    press_card = models.FileField(
        upload_to='membership/press_cards/%Y/', blank=True, null=True,
        verbose_name=_("Press Card / Accreditation (PDF/JPG)")
    )
    photo = models.ImageField(
        upload_to='membership/photos/%Y/', blank=True, null=True,
        verbose_name=_("Passport-size Photo")
    )

    # Workflow
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='draft',
        verbose_name=_("Application Status")
    )
    admin_notes = models.TextField(
        blank=True, verbose_name=_("Admin Notes"),
        help_text=_("Internal notes — not visible to applicant.")
    )
    submitted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Submitted At"))

    # Spam protection
    honeypot = models.CharField(max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = _("Membership Application")
        verbose_name_plural = _("Membership Applications")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} [{self.reference_number}] — {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = f"NUJ-{str(uuid.uuid4()).upper()[:8]}"
        super().save(*args, **kwargs)

    def get_status_color(self):
        colors = {
            'draft': 'gray', 'submitted': 'blue', 'under_review': 'yellow',
            'approved': 'green', 'rejected': 'red', 'needs_clarification': 'orange',
        }
        return colors.get(self.status, 'gray')


class MemberProfile(TimestampedModel):
    """
    Linked user account for approved members — enables member portal login.
    Created automatically when an application is approved.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='member_profile',
        verbose_name=_("User Account")
    )
    application = models.OneToOneField(
        MembershipApplication, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='member_profile', verbose_name=_("Membership Application")
    )
    member_id = models.CharField(
        max_length=20, unique=True, blank=True,
        verbose_name=_("Member ID"),
        help_text=_("Auto-generated unique member number.")
    )
    membership_type = models.CharField(
        max_length=20,
        choices=MembershipApplication.MEMBERSHIP_TYPES,
        default='ordinary',
        verbose_name=_("Membership Type")
    )
    city = models.CharField(max_length=3, choices=INDIAN_STATES, blank=True, verbose_name=_("City"))
    designation = models.CharField(max_length=200, blank=True, verbose_name=_("Designation"))
    organization = models.CharField(max_length=300, blank=True, verbose_name=_("Organization"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    address = models.TextField(blank=True, verbose_name=_("Address"))
    bio = models.TextField(blank=True, verbose_name=_("Short Bio"))
    photo = models.ImageField(
        upload_to='members/photos/%Y/', blank=True, null=True,
        verbose_name=_("Profile Photo")
    )
    press_card = models.FileField(
        upload_to='members/press_cards/%Y/', blank=True, null=True,
        verbose_name=_("Press Card")
    )
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('city_admin', 'City Admin'),
        ('super_admin', 'Super Admin'),
    ]

    is_active_member = models.BooleanField(default=True, verbose_name=_("Active Member"))
    membership_valid_until = models.DateField(
        blank=True, null=True, verbose_name=_("Membership Valid Until")
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='member',
        verbose_name=_("Portal Role"),
        help_text=_("member = normal access; city_admin = manage one city; super_admin = manage everything")
    )
    managed_city = models.CharField(
        max_length=3, choices=INDIAN_STATES, blank=True,
        verbose_name=_("Managed City"),
        help_text=_("For city_admin role only — which city this person manages.")
    )

    class Meta:
        verbose_name = _("Member Profile")
        verbose_name_plural = _("Member Profiles")
        ordering = ['member_id']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} [{self.member_id}]"

    def save(self, *args, **kwargs):
        if not self.member_id:
            import random
            self.member_id = f"NUJUP-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username
