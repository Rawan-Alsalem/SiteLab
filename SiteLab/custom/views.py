from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from .forms import CustomRequestForm, PaymentForm
from .models import CustomRequest


@login_required
def create_request_view(request):
    if request.method == "POST":
        form = CustomRequestForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            messages.success(request, "Your custom request has been submitted successfully!")
            return redirect("custom:my_requests_view")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomRequestForm()
    return render(request, "custom/create_request.html", {"form": form})


@login_required
def my_requests_view(request):
    requests = CustomRequest.objects.filter(user=request.user).order_by("-created_at")
    custom_requests = request.user.custom_requests.all().order_by('-created_at')
    return render(request, "custom/my_requests.html", {"requests": requests, "custom_requests":custom_requests})


@login_required
def request_detail_view(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk, user=request.user)
    back_url = request.GET.get('next') or reverse("custom:my_requests_view")
    return render(request, "custom/request_detail.html", {"req": req, "back_url": back_url})


@login_required
def process_payment_view(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk, user=request.user)

    # Determine where to go back after payment
    back_url = request.GET.get("next") or reverse("custom:request_detail_view", args=[req.pk])

    if request.method == "POST":
        form = PaymentForm(request.POST, deposit_paid=req.deposit_paid)
        if form.is_valid():
            payment_type = form.cleaned_data["payment_type"]

            try:
                with transaction.atomic():
                    if payment_type == "deposit":
                        req.mark_deposit_paid(timezone.now())

                    elif payment_type == "final":
                        if not req.deposit_paid:
                            form.add_error(None, "The deposit must be paid first.")
                            return render(request, "custom/payment.html", {
                                "form": form,
                                "req": req,
                                "back_url": back_url
                            })
                        req.mark_final_paid(timezone.now())

                    req.save()

                return redirect(back_url)

            except Exception as e:
                print("Payment error:", e)
                form.add_error(None, "An error occurred during the payment process.")

    else:
        form = PaymentForm(deposit_paid=req.deposit_paid)

    return render(request, "custom/payment.html", {
        "form": form,
        "req": req,
        "back_url": back_url
    })



@login_required
def edit_request_view(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk, user=request.user)

    if req.status == "completed":
        messages.error(request, "You cannot edit a completed request.")

        back_url = request.GET.get('next') or reverse("custom:request_detail_view", args=[req.pk])
        return redirect(back_url)

    back_url = request.GET.get('next') or reverse("custom:request_detail_view", args=[req.pk])

    if request.method == "POST":
        form = CustomRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been updated successfully!")
            return redirect(back_url)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomRequestForm(instance=req)

    return render(request, "custom/edit_request.html", {
        "form": form,
        "req": req,
        "back_url": back_url
    })

@login_required
def delete_custom_request(request, pk):
    if request.method == "POST":
        req = get_object_or_404(CustomRequest, pk=pk, user=request.user)
        req.delete()
        return redirect('panel:panel_view')
    return redirect('panel:panel_view')


@staff_member_required
@transaction.atomic
def update_status(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status:
            req.status = new_status
            req.save()
        return redirect("/admin/")

    return render(request, "custom/update_status.html", {"req": req})


@staff_member_required
def admin_requests_view(request):
    status_filter = request.GET.get("status")

    requests_qs = CustomRequest.objects.all().order_by("-created_at")

    # Apply filter if selected
    if status_filter and status_filter != "all":
        requests_qs = requests_qs.filter(status=status_filter)

    return render(request, "custom/admin_requests.html", {
        "requests": requests_qs,
        "status_filter": status_filter,
    })


@staff_member_required
def update_status_view(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        req.status = new_status
        req.save()
        return redirect('custom:admin_requests_view')

    return render(request, 'custom/update_status.html', {'req': req})

@staff_member_required
@require_POST
def delete_request_view(request, pk):
    req = get_object_or_404(CustomRequest, pk=pk)
    req.delete()
    messages.success(request, f"Request '{req.project_title}' has been deleted.")
    return redirect("custom:admin_requests_view")