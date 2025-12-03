from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms.models import model_to_dict
from .models import Portfolio
from .forms import PortfolioForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError 

MOCK_REVIEWS = [
    {'username': 'Sarah Jenkins', 'text': 'SiteLab completely transformed my portfolio. I got three job offers within a week of launching!', 'rating': 5, 'initial': 'S'},
    {'username': 'Mark D.', 'text': 'The custom website team is top-tier. They handled our complex requirements with ease.', 'rating': 5, 'initial': 'M'},
    {'username': 'Alex T.', 'text': 'Clean, modern, and super easy to use. I love the new dashboard features.', 'rating': 4.5, 'initial': 'A'},
    {'username': 'Jordan P.', 'text': 'The speed of deployment is incredible. Highly recommend for fast, professional sites.', 'rating': 5, 'initial': 'J'},
    {'username': 'Lena R.', 'text': 'Excellent value for money. The templates are high quality and easy to customize.', 'rating': 4, 'initial': 'L'},
    {'username': 'Chris B.', 'text': 'Needed a professional site fast, and SiteLab delivered. Fantastic support staff!', 'rating': 5, 'initial': 'C'},
]

MOCK_TEMPLATES = [
    {'id': 1, 'name': 'Architect Minimal', 'description': 'A clean, typography-focused design perfect for designers and writers.', 'icon': 'fa-solid fa-pen-nib'},
    {'id': 2, 'name': 'Professional Designer', 'description': 'A modern, image-heavy layout for creative professionals.', 'icon': 'fa-solid fa-palette'},
    {'id': 3, 'name': 'Creative Photographer', 'description': 'Focus on high-resolution imagery and clean grids.', 'icon': 'fa-solid fa-camera'},
    {'id': 4, 'name': 'Developer Terminal', 'description': 'A dark-mode, code-centric theme for software engineers.', 'icon': 'fa-solid fa-terminal'},
]

TEMPLATE_ID_MAP = {t['id']: t for t in MOCK_TEMPLATES}

MOCK_USER_PK = 1


def our_services(request):
    return render(request, 'portfolios/our-services.html', {'reviews': MOCK_REVIEWS})

def portfolio_add(request):
    return render(request, 'portfolios/portfolio-add.html', {'templates': MOCK_TEMPLATES})


def _get_portfolio_instance(user_pk, selected_template_id=1):
    """Fetches or creates the portfolio instance for the mock user."""
    try:
        portfolio = Portfolio.objects.get(pk=user_pk)
        
        if portfolio.template_id != selected_template_id:
             portfolio.template_id = selected_template_id
             portfolio.save() 
        
    except Portfolio.DoesNotExist:
        try:
            User = get_user_model()
            mock_user = User.objects.get(pk=user_pk)
            
            portfolio = Portfolio(
                user=mock_user, 
                template_id=selected_template_id
            )
            
        except User.DoesNotExist:
             print(f"CRITICAL ERROR: Mock User with PK={user_pk} does not exist. Cannot create Portfolio.")
             portfolio = Portfolio(template_id=selected_template_id)
             
    except Exception as e:
        print(f"An unexpected error occurred during portfolio retrieval/creation: {e}")
        portfolio = Portfolio(template_id=selected_template_id)
        
    return portfolio


def portfolio_edit(request):
    selected_template_id = int(request.POST.get('template_id', request.GET.get('template_id', 1)))
    
    portfolio = _get_portfolio_instance(MOCK_USER_PK, selected_template_id)
    
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        
        if form.is_valid():
            
            portfolio_instance = form.save(commit=False)
            
            if not portfolio_instance.pk:
                try:
                    User = get_user_model()
                    portfolio_instance.user = User.objects.get(pk=MOCK_USER_PK)
                except User.DoesNotExist:
                    print(f"CRITICAL ERROR: Mock User with PK={MOCK_USER_PK} does not exist.")
                    return render(request, 'portfolios/error_page.html', {'message': 'User authentication failed.'})


            if 'publish' in request.POST:
                portfolio_instance.is_published = True
                portfolio_instance.save()
                return redirect('portfolios:portfolio_published')

            portfolio_instance.save()
            
            return redirect(f"{redirect('portfolios:portfolio_edit').url}?template_id={portfolio_instance.template_id}")

    else:
        form = PortfolioForm(instance=portfolio)
        
    template_data = TEMPLATE_ID_MAP.get(portfolio.template_id, TEMPLATE_ID_MAP[1])
    
    context = {
        'form': form,
        'template_id': portfolio.template_id,
        'template_name': template_data['name'],
        'preview_data': model_to_dict(portfolio), 
    }
    
    return render(request, 'portfolios/portfolio-edit.html', context)


def portfolio_published(request):
    portfolio_instance, portfolio_data = _get_portfolio_data()
    
    if not portfolio_instance.is_published:
        return redirect(f"{redirect('portfolios:portfolio_edit').url}?template_id={portfolio_instance.template_id}")
        
    live_url = request.build_absolute_uri(redirect('portfolios:published_view').url)
    
    return render(request, 'portfolios/portfolio-published.html', {'live_url': live_url})


def _get_portfolio_data(user_id=MOCK_USER_PK):
    """Helper to fetch or create portfolio data for rendering."""
    try:
        portfolio = Portfolio.objects.get(pk=user_id)
        return portfolio, model_to_dict(portfolio)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio() 
        portfolio.template_id = 1
        return portfolio, model_to_dict(portfolio)


def preview_view(request):
    """
    Renders the live preview in the editor's iframe.
    This view uses the user's SAVED data.
    """
    portfolio_instance, portfolio_data = _get_portfolio_data()
    
    template_path = portfolio_instance.get_template_path()
    template_name = TEMPLATE_ID_MAP.get(portfolio_instance.template_id, TEMPLATE_ID_MAP[1])['name']
    
    context = {
        'portfolio_data': portfolio_data, 
        'template_path': template_path,  
        'template_name': template_name,
    }
    return render(request, 'portfolios/preview.html', context)


def published_view(request):
    """
    Renders the final, live, published site at the user's unique URL.
    This view uses the user's SAVED data.
    """
    portfolio_instance, portfolio_data = _get_portfolio_data()
    
    if not portfolio_instance.is_published:
        return redirect(f"{redirect('portfolios:portfolio_edit').url}?template_id={portfolio_instance.template_id}")
    
    template_path = portfolio_instance.get_template_path()
    template_name = TEMPLATE_ID_MAP.get(portfolio_instance.template_id, TEMPLATE_ID_MAP[1])['name']
    
    context = {
        'portfolio_data': portfolio_data,
        'template_path': template_path,
        'template_name': template_name,
    }
    return render(request, 'portfolios/published.html', context)


def template1_view(request):
    return render(request, 'portfolios/portfolio_template1.html')

def template2_view(request):
    return render(request, 'portfolios/portfolio_template2.html')

def template3_view(request):
    return render(request, 'portfolios/portfolio_template3.html')

def template4_view(request):
    return render(request, 'portfolios/portfolio_template4.html')