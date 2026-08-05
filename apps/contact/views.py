"""
apps/contact/views.py
"""
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

logger = logging.getLogger('apps.contact')


def contact_index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Notify admin
            try:
                send_mail(
                    subject=f"[NUJ India] Contact: {inquiry.subject}",
                    message=f"Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\nDepartment: {inquiry.get_department_display()}\nSubject: {inquiry.subject}\n\nMessage:\n{inquiry.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Contact email failed: {e}")

            messages.success(request, "Thank you for contacting us. We will get back to you within 2-3 business days.")
            return redirect('contact:index')
    else:
        form = ContactForm()

    return render(request, 'contact/index.html', {
        'form': form,
        'breadcrumbs': [('Contact', None)],
        'page_title': 'Contact Us — NUJ India',
    })
