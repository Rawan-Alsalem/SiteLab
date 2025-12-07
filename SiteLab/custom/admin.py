from django.contrib import admin
from .models import CustomRequest

@admin.register(CustomRequest)
class CustomRequestAdmin(admin.ModelAdmin):
    list_display = (
        "project_title",
        "user",
        "project_type",
        "project_focus",
        "budget_range",
        "status",
        "deposit_paid",
        "final_paid",
        "created_at",
    )

    list_filter = (
        "status",
        "project_type",
        "project_focus",
        "deposit_paid",
        "final_paid",
        "created_at",
    )

    search_fields = ("project_title", "user__username", "name", "email")

    readonly_fields = (
        "created_at",
        "updated_at",
        "deposit_paid_at",
        "final_paid_at",
    )