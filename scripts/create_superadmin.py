"""
scripts/create_superadmin.py
Run via: python manage.py shell < scripts/create_superadmin.py
Creates or verifies the portal Super Admin account.
"""
from django.contrib.auth import get_user_model
from apps.membership.models import MemberProfile

User = get_user_model()

# Create or get the superadmin user
user, created = User.objects.get_or_create(
    username='superadmin',
    defaults={
        'email': 'superadmin@nujup.org',
        'first_name': 'Super',
        'last_name': 'Admin',
        'is_staff': True,
    }
)

if created:
    user.set_password('NujUp@2024')
    user.save()
    print(f"[OK] Created user: superadmin")
else:
    print(f"[OK] User already exists: superadmin")

# Create or get the MemberProfile with super_admin role
try:
    profile = user.member_profile
    if profile.role != 'super_admin':
        profile.role = 'super_admin'
        profile.is_active_member = True
        profile.save()
        print(f"[OK] Updated profile role to super_admin")
    else:
        print(f"[OK] Profile already has super_admin role")
except MemberProfile.DoesNotExist:
    MemberProfile.objects.create(
        user=user,
        role='super_admin',
        is_active_member=True,
    )
    print(f"[OK] Created MemberProfile with super_admin role")

print()
print("=" * 48)
print("  Portal Super Admin account ready:")
print("  Username : superadmin")
print("  Password : NujUp@2024")
print("  URL      : /portal/admin-panel/")
print("=" * 48)
