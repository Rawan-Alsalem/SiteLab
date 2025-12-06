from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from portfolios.models import Portfolio, PortfolioTemplate
from portfolios.forms import PortfolioForm
from custom.models import CustomRequest
from custom.forms import CustomRequestForm
from panel.models import Review
from panel.forms import ReviewForm
from accounts.models import PrivacySettings
from accounts.forms import PrivacySettingsForm

@login_required
def panel_view(request):
    user = request.user

    # ---------- Portfolio ----------
    portfolio = getattr(user, 'portfolio', None)
    portfolio_form = PortfolioForm(request.POST or None, request.FILES or None, instance=portfolio)
    if request.method == "POST" and "save_portfolio" in request.POST:
        if portfolio_form.is_valid():
            p = portfolio_form.save(commit=False)
            p.user = user
            p.save()
            messages.success(request, "Portfolio updated successfully!")
            return redirect('panel:panel_view')

    # ---------- Reviews ----------
    reviews = user.reviews.all().order_by('-created_at')
    review_form = ReviewForm(request.POST or None)
    if request.method == "POST" and "add_review" in request.POST:
        if review_form.is_valid():
            r = review_form.save(commit=False)
            r.user = user
            r.save()
            messages.success(request, "Review added successfully!")
            return redirect('panel:panel_view')

    # ---------- Custom Requests ----------
    custom_requests = user.custom_requests.all().order_by('-created_at')
    custom_form = CustomRequestForm(request.POST or None)

    # ---------- Privacy Settings ----------
    privacy, created = PrivacySettings.objects.get_or_create(user=user)
    privacy_form = PrivacySettingsForm(request.POST or None, instance=privacy)
    if request.method == "POST" and "save_privacy" in request.POST:
        if privacy_form.is_valid():
            privacy_form.save()
            messages.success(request, "Privacy settings updated successfully!")
            return redirect('panel:panel_view')

    # ---------- Recent Activity ----------
    recent_actions = []
    if portfolio:
        recent_actions.append({
            "type": "Portfolio",
            "title": portfolio.template.name if portfolio.template else "No Template",
            "date": portfolio.last_updated
        })
    for r in reviews[:5]:
        recent_actions.append({
            "type": "Review",
            "title": r.review_text[:50],
            "date": r.created_at
        })
    for req in custom_requests[:5]:
        recent_actions.append({
            "type": "Custom Request",
            "title": req.project_title,
            "date": req.updated_at if req.updated_at else req.created_at
        })
    recent_actions = sorted(recent_actions, key=lambda x: x["date"], reverse=True)

    context = {
        'portfolio': portfolio,
        'portfolio_form': portfolio_form,
        'reviews': reviews,
        'review_form': review_form,
        'custom_requests': custom_requests,
        'custom_form': custom_form,
        'privacy_form': privacy_form,
        'recent_actions': recent_actions,
    }

    return render(request, 'panel/user_panel.html', context)



# ---------------- DELETE FUNCTIONS ----------------
@login_required
def delete_portfolio(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    portfolio.delete()
    messages.success(request, "Portfolio deleted successfully!")
    return redirect('panel:panel_view')


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('panel:panel_view')


@login_required
def delete_custom_request(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk, user=request.user)
    req.delete()
    messages.success(request, "Custom request deleted successfully!")
    return redirect('panel:panel_view')



@login_required
def add_review(request):
    success_message = None

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            success_message = "Thank you! Your review has been submitted."
            form = ReviewForm()
    else:
        form = ReviewForm()

    return render(request, 'panel/add_review.html', {
        'form': form,
        'success_message': success_message
    })


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('panel:panel_view')


@login_required
@require_POST
def delete_custom_request(request, request_id):
    req = get_object_or_404(CustomRequest, pk=request_id, user=request.user)
    req.delete()
    return redirect('panel:panel_view')