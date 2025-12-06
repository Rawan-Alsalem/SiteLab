from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)

    USERNAME_FIELD = 'email' 

    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    class Meta:
        db_table = "CustomUser"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
   
class PrivacySettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="privacy_settings")
    show_email = models.BooleanField(default=True, help_text="Allow others to see your email")
    show_bio = models.BooleanField(default=True, help_text="Allow others to see your bio")
    show_portfolio = models.BooleanField(default=True, help_text="Allow others to see your portfolio")

    def __str__(self):
        return f"Privacy Settings for {self.user.username}"