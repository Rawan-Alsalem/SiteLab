from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

class PortfolioTemplate(models.Model):
    """
    Stores available portfolio template designs.
    """
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="FontAwesome class, e.g., 'fa-solid fa-camera'")
    description = models.TextField(default="", blank=True)
    
    full_name = models.CharField(max_length=100, default="Samantha J. Doe")
    tagline = models.CharField(max_length=255, default="Senior UX/UI Designer & Web Developer")
    about_me = models.TextField(default="A seasoned professional dedicated to crafting visually stunning and highly functional digital experiences.")
    contact_email = models.EmailField(default="contact@samanthajdoe.com")

    project_title = models.CharField(max_length=255, default="Sample Project")
    project_description = models.TextField(default="A sample project description to showcase the template layout.")
    project_url = models.URLField(
        max_length=255,
        default="https://example.com",
        help_text="Example project link"
    )

    template_path = models.CharField(
        max_length=255,
        default="portfolios/portfolio_template1.html",
        help_text="Path to the HTML template"
    )

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="portfolio"
    )

    template = models.ForeignKey(
        PortfolioTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portfolios"
    )

    is_published = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"

    def get_template_path(self):
        """
        Returns the template path based on the template_id.
        Used for dynamic inclusion in preview/published views.
        """
        return self.template.template_path if self.template else "portfolios/default.html"

        


        