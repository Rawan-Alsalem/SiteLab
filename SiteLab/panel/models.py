from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def username(self):

        return self.user.username if self.user else "Anonymous"

    @property
    def initial(self):
        return self.user.username[0].upper() if self.user else "?"

    def __str__(self):
        return f"{self.username} ({self.rating}★)"

