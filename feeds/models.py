from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Feed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(blank=True, null=True,
                            default="https://www.pngarts.com/files/5/User-Avatar-PNG-Transparent-Image.png")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
                              default='pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username + "==>" + self.to_user.username
