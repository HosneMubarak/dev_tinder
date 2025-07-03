from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.email


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
