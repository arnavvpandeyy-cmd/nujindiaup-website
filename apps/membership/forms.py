"""
apps/membership/forms.py

Membership application form with honeypot anti-spam.
"""
from django import forms
from .models import MembershipApplication
from apps.people.models import INDIAN_STATES


class MembershipApplicationForm(forms.ModelForm):
    """
    Public-facing membership application form.
    Includes a honeypot field to detect bot submissions.
    """
    # Honeypot field — must remain blank; bots tend to fill all fields
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='',
    )

    class Meta:
        model = MembershipApplication
        fields = [
            'full_name', 'email', 'phone', 'dob', 'address', 'state', 'pincode',
            'designation', 'organization', 'experience_years', 'membership_type',
            'id_proof', 'press_card', 'photo',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your residential address'}),
            'state': forms.Select(choices=[('', '— Select City —')] + list(INDIAN_STATES)),
            'pincode': forms.TextInput(attrs={'placeholder': '110001'}),
            'designation': forms.TextInput(attrs={'placeholder': 'e.g., Senior Reporter'}),
            'organization': forms.TextInput(attrs={'placeholder': 'e.g., The Hindu, PTI, Doordarshan'}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 60}),
        }
        labels = {
            'dob': 'Date of Birth',
            'id_proof': 'Identity Proof (PDF or JPG, max 5MB)',
            'press_card': 'Press Card / Accreditation (PDF or JPG, max 5MB)',
            'photo': 'Passport-size Photo (JPG/PNG, max 2MB)',
        }

    def clean_website(self):
        """Honeypot: reject if the hidden field is filled."""
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError("Bot detected.")
        return value

    def clean_experience_years(self):
        years = self.cleaned_data.get('experience_years', 0)
        if years < 0:
            raise forms.ValidationError("Experience years cannot be negative.")
        return years

    def clean_id_proof(self):
        file = self.cleaned_data.get('id_proof')
        if file:
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large. Maximum size is 5MB.")
        return file

    def clean_press_card(self):
        file = self.cleaned_data.get('press_card')
        if file:
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large. Maximum size is 5MB.")
        return file

    def clean_photo(self):
        file = self.cleaned_data.get('photo')
        if file:
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Photo must be JPG or PNG.")
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Photo too large. Maximum size is 2MB.")
        return file


class ApplicationStatusForm(forms.Form):
    """
    Public form to check membership application status by reference number.
    """
    reference_number = forms.CharField(
        max_length=20,
        label='Reference Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., NUJ-XXXXXXXX',
            'autocomplete': 'off',
        })
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email used during application',
        })
    )
