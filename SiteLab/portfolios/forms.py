from django import forms
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['template', 'is_published']

        widgets = {
            'template': forms.Select(attrs={
                'class': 'form-select',
            }),

            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
