from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'minimal-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message', 'class': 'minimal-input'}),
        }