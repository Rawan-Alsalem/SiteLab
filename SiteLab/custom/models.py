from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ====== Choices ======
PROJECT_TYPE_CHOICES = [
    ("website", "Website"),
    ("mobile_app", "Mobile App"),
    ("branding", "Branding"),
    ("other", "Other"),
]

PROJECT_FOCUS_CHOICES = [
    ("design", "Design"),
    ("development", "Development"),
    ("marketing", "Marketing"),
    ("other", "Other"),
]

BUDGET_RANGE_CHOICES = [
    ("<500", "Less than $500"),
    ("500-1000", "$500 - $1000"),
    ("1000-5000", "$1000 - $5000"),
    (">5000", "More than $5000"),
]

STATUS_CHOICES = [
    ("pending", "Pending Review"),
    ("in_progress", "In Progress"),
    ("waiting_payment", "Waiting Final Payment"),
    ("completed", "Completed"),
    ("rejected", "Rejected"),
]


# ====== CustomRequest Model ======
class CustomRequest(models.Model):
    # User & Project Info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_requests")
    name = models.CharField(max_length=150)
    email = models.EmailField()
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    project_focus = models.CharField(max_length=50, choices=PROJECT_FOCUS_CHOICES)
    budget_range = models.CharField(max_length=50, choices=BUDGET_RANGE_CHOICES)
    project_title = models.CharField(max_length=200)
    requirements = models.TextField() 
    sample_links = models.TextField(blank=True, null=True)

    # Payment Fields
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_paid = models.BooleanField(default=False)
    final_paid = models.BooleanField(default=False)
    deposit_paid_at = models.DateTimeField(null=True, blank=True)
    final_paid_at = models.DateTimeField(null=True, blank=True)

    # Status & Timestamps
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ====== Payment Methods ======
    def mark_deposit_paid(self, timestamp):
        self.deposit_paid = True
        self.deposit_paid_at = timestamp
        if not self.final_paid:
            self.status = "in_progress"

    def mark_final_paid(self, timestamp):
        self.final_paid = True
        self.final_paid_at = timestamp
        self.status = "completed"

    def __str__(self):
        return f"{self.project_title} - {self.user.username}"
