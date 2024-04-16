from django.db import models
from django.contrib.auth.models import User


class CrackedPassword(models.Model):
    md5_hash = models.CharField(max_length=32)  # MD5 hashes have a length of 32 characters
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_cracked = models.BooleanField(default=False)
    cracked_password = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.md5_hash} by {self.user.username}"

