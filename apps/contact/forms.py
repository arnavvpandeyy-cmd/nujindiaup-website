"""
apps/contact/forms.py
"""
from django import forms
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    """Contact inquiry form with honeypot."""
    # Honeypot
    website = forms.CharField(required=False, widget=forms.HiddenInput(), label='')

    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'department', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX (optional)'}),
            'department': forms.Select(),
            'subject': forms.TextInput(attrs={'placeholder': 'Brief subject of your inquiry'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your inquiry...'}),
        }

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError("Bot detected.")
        return value

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 20:
            raise forms.ValidationError("Please provide a more detailed message (at least 20 characters).")
        return message
