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
