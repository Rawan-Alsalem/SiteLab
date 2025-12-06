from django import forms
from django.forms.widgets import CheckboxInput
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, User
from .models import PrivacySettings

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Username'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Email'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get("password")
        cp = cleaned.get("confirm_password")
        if p != cp:
            raise forms.ValidationError("Passwords do not match")
        return cleaned
    
    def save(self, commit=True):
        # استدعاء دالة save الأصلية لكن لا تقم بحفظها في قاعدة البيانات (commit=False)
        user = super().save(commit=False)
        
        # استخدام set_password لتشفير كلمة المرور وتعيينها للمستخدم
        # هذا يضمن أن كلمة المرور مشفرة قبل الحفظ
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            
        return user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Password'
    }))

class ProfileForm(forms.ModelForm):
    avatar_clear = forms.BooleanField(required=False, widget=CheckboxInput)
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'minimal-input',
        'placeholder': 'Email'
    }))

    class Meta:
        model = Profile
        fields = ["avatar", "job_title", "bio"]
        widgets = {
            "avatar": forms.FileInput(attrs={
                'class': 'hidden-file-input',
                'id': 'id_avatar'
            }),
            "job_title": forms.TextInput(attrs={
                'class': 'minimal-input',
                'placeholder': 'Job Title'
            }),
            "bio": forms.Textarea(attrs={
                'class': 'minimal-input',
                'rows': 4,
                'placeholder': 'Bio'
            }),
        }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['email'].initial = user_instance.email

    def save(self, commit=True):
        profile_instance = super().save(commit=False)
        
        
        if self.cleaned_data.get('avatar_clear') and profile_instance.avatar:
            profile_instance.avatar.delete(save=False)

        user = profile_instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            profile_instance.save()
        return profile_instance

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = ['show_email', 'show_bio', 'show_portfolio']
        widgets = {
            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_bio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_portfolio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
