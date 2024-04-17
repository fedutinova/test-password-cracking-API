from django.db import models
from django.contrib.auth.models import User


class CrackedPassword(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='crack_attempts')
    md5_hash = models.CharField(max_length=32)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_cracked = models.BooleanField(default=False)
    cracked_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Attempt on {self.md5_hash} {'successful' if self.is_cracked else 'failed'} by {self.user.username}"
