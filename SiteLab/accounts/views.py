import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db import transaction
from .forms import RegisterForm, LoginForm, ProfileForm, PrivacySettingsForm
from .models import Profile, User, PrivacySettings


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save() 
            
            Profile.objects.create(user=user) 
            
            messages.success(request, "Account created successfully!")
            return redirect("accounts:login_view")
    else:
        form = RegisterForm()

    return render(request, "accounts/sign-up.html", {"form": form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or '/'  # fallback to home
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)  # <-- redirect to the next page
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form, "next": next_url})



@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login_view")


@login_required
def profile_view(request):
    profile = request.user.profile
    colors = ['#F87171','#FBBF24','#34D399','#60A5FA','#A78BFA','#F472B6']
    random_color = random.choice(colors)
    active_tab = 'profileTab'

    if request.method == "POST":
        if 'save_profile' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile, user_instance=request.user)
            password_form = PasswordChangeForm(user=request.user)
            active_tab = 'profileTab'

            if profile_form.is_valid():
                try:
                    with transaction.atomic():
                        profile_form.save()
                    messages.success(request, "Profile updated successfully!")
                    return redirect("accounts:profile_view")
                except Exception:
                    messages.error(request, "Error while updating profile. Please try again.")
        elif 'change_password' in request.POST:
            profile_form = ProfileForm(instance=profile, user_instance=request.user)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            active_tab = 'passwordTab'

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect("accounts:profile_view")

    else:
        profile_form = ProfileForm(instance=profile, user_instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    avatar_url = None
    if profile.avatar:
        try:
            avatar_url = profile.avatar.url
        except:
            avatar_url = None

    return render(request, "accounts/profile.html", {
        "profile_form": profile_form,
        "password_form": password_form,
        "random_color": random_color,
        "active_tab": active_tab,
        "avatar_url": avatar_url,
    })


@login_required
def privacy_settings_view(request):
    settings, created = PrivacySettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PrivacySettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Privacy settings updated successfully!")
            return redirect("panel:panel_view")
    else:
        form = PrivacySettingsForm(instance=settings)

    return render(request, "accounts/privacy_settings.html", {"form": form})
