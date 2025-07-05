from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
                              default='pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username + "==>" + self.to_user.username

class NotInterestedUser(models.Model):
    user = models.ForeignKey(User, related_name='not_interested_by', on_delete=models.CASCADE)
    not_interested_user = models.ForeignKey(User, related_name='not_interested_users', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'not_interested_user')

    def __str__(self):
        return f"{self.user.username} is not interested in {self.not_interested_user.username}"
