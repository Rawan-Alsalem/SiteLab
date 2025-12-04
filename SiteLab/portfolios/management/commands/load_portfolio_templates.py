from django.core.management.base import BaseCommand
from portfolios.models import PortfolioTemplate

class Command(BaseCommand):
    help = "Load mock portfolio templates into the database"

    def handle(self, *args, **kwargs):
        MOCK_TEMPLATES = [
            {'name': 'Architect Minimal', 'description': 'A clean, typography-focused design perfect for designers and writers.', 'icon': 'fa-solid fa-pen-nib', 'template_path': 'portfolios/arch_minimal.html'},
            {'name': 'Professional Designer', 'description': 'A modern, image-heavy layout for creative professionals.', 'icon': 'fa-solid fa-palette', 'template_path': 'portfolios/pro_designer.html'},
            {'name': 'Creative Photographer', 'description': 'Focus on high-resolution imagery and clean grids.', 'icon': 'fa-solid fa-camera', 'template_path': 'portfolios/creative_photographer.html'},
            {'name': 'Developer Terminal', 'description': 'A dark-mode, code-centric theme for software engineers.', 'icon': 'fa-solid fa-terminal', 'template_path': 'portfolios/dev_terminal.html'},
        ]

        for tmpl in MOCK_TEMPLATES:
            PortfolioTemplate.objects.update_or_create(
                name=tmpl['name'],
                defaults={
                    'description': tmpl['description'],
                    'icon': tmpl['icon'],
                    'template_path': tmpl['template_path'],
                }
            )
        self.stdout.write(self.style.SUCCESS("Portfolio templates loaded successfully."))