from django import forms
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    """
    Form based on the Portfolio model for use in the editor.
    This form handles all editable fields defined in models.py.
    """
    class Meta:
        model = Portfolio
        # Specify all fields the user can edit in the editor
        fields = [
            'template_id', 
            'name', 
            'tagline', 
            'about_me', 
            'contact_email', 
            'project_title_1', 
            'project_description_1', 
            'project_url_1'
        ]
        
        # Customize the widgets for better UX in the editor
        widgets = {
            'template_id': forms.HiddenInput(), # Hidden, as it's set on creation
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Jane Doe'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior UX Designer'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'A concise professional summary.'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g., hello@janedoe.com'}),
            'project_title_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., E-Commerce Platform Redesign'}),
            'project_description_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed results and role in the project.'}),
            'project_url_1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional: https://case-study.com'}),
        }