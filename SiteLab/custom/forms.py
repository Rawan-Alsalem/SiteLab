from django import forms
from .models import CustomRequest

# ====== Custom Request Form ======
class CustomRequestForm(forms.ModelForm):
    class Meta:
        model = CustomRequest
        fields = [
            "name",
            "email",
            "project_type",
            "project_focus",
            "budget_range",
            "project_title",
            "requirements",
            "sample_links",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} minimal-input".strip()

        # placeholders
        self.fields["name"].widget.attrs["placeholder"] = "Enter your full name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email address"
        self.fields["project_title"].widget.attrs["placeholder"] = "Enter a catchy project title"
        self.fields["requirements"].widget.attrs.update({
            "rows": 5,
            "placeholder": "Describe your project, key features, and any specific technologies or deadlines.",
        })
        self.fields["sample_links"].widget.attrs.update({
            "rows": 2,
            "placeholder": "Add any sample links or references (optional).",
        })


# ====== Payment Form ======
class PaymentForm(forms.Form):
    payment_type = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        deposit_paid = kwargs.pop("deposit_paid", False)
        super().__init__(*args, **kwargs)

        choices = [("deposit", "Deposit Payment")]
        if deposit_paid:
            choices.append(("final", "Final Payment"))

        self.fields["payment_type"].choices = choices
        self.fields["payment_type"].widget.attrs.update({
            "class": "minimal-input"
        })
