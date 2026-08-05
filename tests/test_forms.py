"""
tests/test_forms.py

Unit tests for NUJ India forms.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.contact.forms import ContactForm
from apps.membership.forms import MembershipApplicationForm, ApplicationStatusForm
from apps.membership.models import MembershipApplication


class ContactFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+91 9876543210',
            'department': 'general',
            'subject': 'Test Subject',
            'message': 'This is a test message that is long enough.',
            'website': '',  # honeypot must be empty
        }
        form = ContactForm(data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_honeypot_rejection(self):
        data = {
            'name': 'Bot',
            'email': 'bot@spam.com',
            'department': 'general',
            'subject': 'Spam',
            'message': 'This is bot spam content here okay.',
            'website': 'http://spamsite.com',  # honeypot filled
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())

    def test_short_message_rejected(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'general',
            'subject': 'Hi',
            'message': 'Hi',  # too short
            'website': '',
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_invalid_email(self):
        data = {
            'name': 'Test User',
            'email': 'not-an-email',
            'department': 'general',
            'subject': 'Test Subject',
            'message': 'This is a test message that is long enough.',
            'website': '',
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())


class MembershipApplicationFormTest(TestCase):

    def _valid_data(self):
        return {
            'full_name': 'Rahul Sharma',
            'email': 'rahul@example.com',
            'phone': '+91 9876543210',
            'dob': '1985-06-15',
            'address': '123 Main Street, New Delhi',
            'state': 'DL',
            'pincode': '110001',
            'designation': 'Senior Reporter',
            'organization': 'The Hindu',
            'experience_years': 10,
            'membership_type': 'ordinary',
            'website': '',  # honeypot
        }

    def test_valid_form_without_files(self):
        form = MembershipApplicationForm(self._valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_honeypot_rejection(self):
        data = self._valid_data()
        data['website'] = 'http://spam.com'
        form = MembershipApplicationForm(data)
        self.assertFalse(form.is_valid())

    def test_negative_experience_rejected(self):
        data = self._valid_data()
        data['experience_years'] = -5
        form = MembershipApplicationForm(data)
        self.assertFalse(form.is_valid())


class ContactViewTest(TestCase):

    def setUp(self):
        # Create SiteSettings singleton
        from apps.core.models import SiteSettings
        SiteSettings.objects.get_or_create(pk=1)

    def test_contact_page_get(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send an Inquiry')

    def test_contact_form_submission(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'general',
            'subject': 'Test Inquiry',
            'message': 'This is a valid test message for the form.',
            'website': '',
        }
        response = self.client.post('/contact/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        from apps.contact.models import ContactInquiry
        self.assertEqual(ContactInquiry.objects.count(), 1)


class MembershipModelTest(TestCase):

    def test_reference_number_generated(self):
        app = MembershipApplication.objects.create(
            full_name='Test Journalist',
            email='test@example.com',
            phone='+91 9876543210',
            dob='1990-01-01',
            address='Test Address',
            state='DL',
            designation='Reporter',
            organization='Test Media',
        )
        self.assertIsNotNone(app.reference_number)
        self.assertTrue(app.reference_number.startswith('NUJ-'))

    def test_status_default_is_draft(self):
        app = MembershipApplication.objects.create(
            full_name='Test Journalist',
            email='test2@example.com',
            phone='+91 9876543210',
            dob='1990-01-01',
            address='Test Address',
            state='MH',
            designation='Reporter',
            organization='Test Media',
        )
        self.assertEqual(app.status, 'draft')
