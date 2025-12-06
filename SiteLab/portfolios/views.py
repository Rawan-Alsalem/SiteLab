from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Portfolio, PortfolioTemplate
from .forms import PortfolioForm

from django.views.decorators.clickjacking import xframe_options_exempt

import json
from django.http import JsonResponse
from django.db import IntegrityError 

User = get_user_model()


def portfolio_add(request):
    """
    Template selection page.
    """
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/portfolio-add.html', {'templates': templates})


@login_required
def portfolio_edit(request):
    """
    Edit the user's Portfolio.
    Supports AJAX auto-save + live preview.
    """
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    
    template_id = request.GET.get('template_id')
    if template_id and (created or not portfolio.template or str(portfolio.template.id) != template_id):
        try:
            new_template = PortfolioTemplate.objects.get(id=template_id)
            portfolio.template = new_template
            portfolio.save() 
            
            if created or str(portfolio.template.id) != template_id:
                t = portfolio.template
                portfolio.first_name = portfolio.first_name or t.default_first_name
                portfolio.last_name = portfolio.last_name or t.default_last_name
                portfolio.tagline = portfolio.tagline or t.default_tagline
                portfolio.about_me = portfolio.about_me or t.default_about_me
                portfolio.contact_email = portfolio.contact_email or t.default_contact_email

                portfolio.save()

            return redirect("portfolios:portfolio_edit")

        except PortfolioTemplate.DoesNotExist:
            pass 

    
    if not portfolio.template:
         return redirect("portfolios:portfolio_add")


    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try:
            data = json.loads(request.body)
            allowed_fields = [
                'first_name', 'last_name', 'tagline', 'about_me', 'contact_email',
                'project1_title', 'project1_description', 'project1_url',
                'project2_title', 'project2_description', 'project2_url',
                'project3_title', 'project3_description', 'project3_url',
            ]
            
            updates = False
            for field, value in data.items():
                if field in allowed_fields:
                    setattr(portfolio, field, value)
                    updates = True
            
            if updates:
                portfolio.save(update_fields=data.keys()) 
            
            return JsonResponse({'status': 'saved', 'message': 'Portfolio auto-saved.'})
        
        except (json.JSONDecodeError, IntegrityError, TypeError) as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid request or database error: {e}'}, status=400)
    

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            
            if 'publish_site' in request.POST:
                portfolio.is_published = True
                portfolio.save(update_fields=['is_published'])
                return redirect("portfolios:publish_success")
            
            elif 'unpublish_site' in request.POST:
                portfolio.is_published = False
                portfolio.save(update_fields=['is_published'])
                return redirect("portfolios:portfolio_edit") 

            return redirect("portfolios:portfolio_edit")
        

    form = PortfolioForm(instance=portfolio) 
    
    context = {
        "form": form,
        "portfolio": portfolio,
        "template_name": portfolio.template.name,
        "template_id": portfolio.template.id,
        "preview_url": reverse("portfolios:preview_view"),
        "published_url": reverse("portfolios:published_view", args=[request.user.username]),
    }
    return render(request, 'portfolios/portfolio-edit.html', context)


@login_required
def portfolio_published(request):
    """
    Landing page after publishing. (Success Message - maps to publish_success URL)
    """
    portfolio = get_object_or_404(Portfolio, user=request.user)

    if not portfolio.is_published:
        return redirect("portfolios:portfolio_edit")

    live_url = request.build_absolute_uri(
        reverse("portfolios:published_view", args=[request.user.username])
    )

    context = {
        "portfolio": portfolio,
        "live_url": live_url,
        "template_path": portfolio.get_template_path(),
    }
    return render(request, 'portfolios/publish_success.html', context)


@xframe_options_exempt
def preview_view(request):
    """
    View used inside the iframe for the live preview.
    Uses @xframe_options_exempt to allow it to be embedded.
    """
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return render(request, "portfolios/preview.html", {
            "template_path": None,
            "template_name": None,
            "portfolio": None,
        })

    template_path = portfolio.get_template_path()

    return render(request, "portfolios/preview.html", {
        "portfolio": portfolio,
        "template_path": template_path,
        "template_name": portfolio.template.name if portfolio.template else "",
    })


def published_view(request, username):
    """
    Public published site for the given username. (Template Wrapper - maps to portfolio_live template)
    """
    user = get_object_or_404(User, username=username)
    portfolio = get_object_or_404(Portfolio, user=user)

    if not portfolio.is_published:
        return render(request, 'main/404.html', status=404) 

    context = {
        "portfolio": portfolio,
        "template_path": portfolio.get_template_path(),
        "template_name": portfolio.template.name if portfolio.template else "",
    }
    return render(request, 'portfolios/portfolio_live.html', context)


def template1_view(request):
    return render(request, 'portfolios/portfolio_template1.html')

def template2_view(request):
    return render(request, 'portfolios/portfolio_template2.html')

def template3_view(request):
    return render(request, 'portfolios/portfolio_template3.html')

def template4_view(request):
    return render(request, 'portfolios/portfolio_template4.html')