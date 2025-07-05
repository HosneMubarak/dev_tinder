from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    photo = models.URLField(
        blank=True,
        null=True,
        default="https://www.pngarts.com/files/5/User-Avatar-PNG-Transparent-Image.png"
    )
    about = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True, default=list)  # Default empty list for safety

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
