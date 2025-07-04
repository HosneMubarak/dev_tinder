from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Feed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(blank=True, null=True, default="https://www.pngarts.com/files/5/User-Avatar-PNG-Transparent-Image.png")
    about = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.email


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
