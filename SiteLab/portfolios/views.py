from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import IntegrityError

from .models import Portfolio, PortfolioTemplate
from .forms import PortfolioForm

MOCK_USER_PK = 1

User = get_user_model()


def portfolio_add(request):
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/portfolio-add.html', {'templates': templates})


def _get_portfolio_instance(user_pk, selected_template_id=1):
    """Fetch or create a Portfolio instance for a user PK (returns unsaved instance for create branch)."""
    try:
        portfolio = Portfolio.objects.get(user__pk=user_pk)

        if portfolio.template_id != int(selected_template_id):
            portfolio.template_id = int(selected_template_id)
            portfolio.save()

    except Portfolio.DoesNotExist:
        try:
            mock_user = User.objects.get(pk=user_pk)
            portfolio = Portfolio(user=mock_user, template_id=selected_template_id)
        except User.DoesNotExist:
            print(f"CRITICAL ERROR: Mock User with PK={user_pk} does not exist. Returning unsaved Portfolio.")
            portfolio = Portfolio(template_id=selected_template_id)

    except Exception as e:
        print(f"An unexpected error occurred during portfolio retrieval/creation: {e}")
        portfolio = Portfolio(template_id=selected_template_id)

    return portfolio

@login_required
def portfolio_edit(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)

    selected_template_id = request.GET.get('template_id') or request.GET.get('template')
    if selected_template_id:
        try:
            portfolio.template = PortfolioTemplate.objects.get(pk=selected_template_id)
            portfolio.save()
        except PortfolioTemplate.DoesNotExist:
            pass

    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            if 'publish' in request.POST:
                portfolio.is_published = True
            portfolio.save()
            return redirect("portfolios:portfolio_edit")
    else:
        form = PortfolioForm(instance=portfolio)

    return render(request, "portfolios/portfolio-edit.html", {
        "form": form,
        "current_template": portfolio.template,
        "templates": PortfolioTemplate.objects.all(),
        "template_id": portfolio.template_id,
        "template_name": portfolio.template.name if portfolio.template else "",
    })


def portfolio_published(request):
    portfolio_instance, portfolio_data = _get_portfolio_data()

    if not portfolio_instance.is_published:
        edit_url = reverse('portfolios:portfolio_edit')
        return redirect(f"{edit_url}?template_id={portfolio_instance.template_id}")

    live_url = request.build_absolute_uri(reverse('portfolios:published_view', args=(portfolio_instance.user.username,)))
    return render(request, 'portfolios/portfolio-published.html', {'live_url': live_url})


def _get_portfolio_data(user_id=None):
    """
    Helper to fetch or create portfolio data for rendering.
    If user_id is None, it will try MOCK_USER_PK (dev-only).
    """
    if user_id is None:
        user_id = MOCK_USER_PK

    try:
        portfolio = Portfolio.objects.get(user__pk=user_id)
        return portfolio, model_to_dict(portfolio)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio()
        portfolio.template_id = 1
        return portfolio, model_to_dict(portfolio)
    except Exception as e:
        print(f"Error fetching portfolio data: {e}")
        portfolio = Portfolio()
        portfolio.template_id = 1
        return portfolio, model_to_dict(portfolio)


@login_required
def preview_view(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)

    return render(request, 'portfolios/preview.html', {
        "portfolio": portfolio,
        "template_path": portfolio.get_template_path(),
        "template": portfolio.template
    })


def published_view(request, username):
    user = get_object_or_404(User, username=username)
    portfolio = get_object_or_404(Portfolio, user=user)

    if not portfolio.is_published:
        return redirect("portfolios:portfolio_edit")

    return render(request, 'portfolios/published.html', {
        "portfolio": portfolio,
        "template_path": portfolio.get_template_path(),
        "template": portfolio.template
    })


def template1_view(request):
    return render(request, 'portfolios/portfolio_template1.html')


def template2_view(request):
    return render(request, 'portfolios/portfolio_template2.html')


def template3_view(request):
    return render(request, 'portfolios/portfolio_template3.html')


def template4_view(request):
    return render(request, 'portfolios/portfolio_template4.html')
