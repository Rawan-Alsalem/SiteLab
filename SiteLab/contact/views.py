from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Contact
from .forms import ContactForm


def contact_view(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user if request.user.is_authenticated else None
            contact.save()

            # Send Confirmation Email
            content_html = render_to_string("contact/mail/confirmation.html", {'contact': contact})
            email_message = EmailMessage(
                subject="Confirmation",
                body=content_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[contact.email]
            )
            email_message.content_subtype = "html"
            email_message.send()
            
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact:contact_view')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


# Custom decorator to show a message if user is not superuser
def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view, login_url='/login/')


# Contact Us Messages page (admin)
@staff_member_required
def contact_messages_view(request):
    messages_list = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/contact_messages.html', {'messages_list': messages_list})