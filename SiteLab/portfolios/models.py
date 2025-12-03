from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

class Portfolio(models.Model):
    """
    Represents a user's customizable portfolio website.
    It contains content fields and configuration settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    template_id = models.IntegerField(default=1) 
    
    full_name = models.CharField(max_length=100, default="Samantha J. Doe")
    tagline = models.CharField(max_length=255, default="Senior UX/UI Designer & Web Developer")
    about_me = models.TextField(default="A seasoned professional dedicated to crafting visually stunning and highly functional digital experiences.")
    contact_email = models.EmailField(default="contact@samanthajdoe.com")
    
    is_published = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Portfolio for {self.full_name} (T{self.template_id})"

    def get_template_path(self):
        """
        Returns the template path based on the template_id.
        Used for dynamic inclusion in preview/published views.
        """
        return f'portfolios/portfolio_template{self.template_id}.html'