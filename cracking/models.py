from django.db import models
from django.contrib.auth.models import User



class CrackedPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cracked_passwords")
    md5_hash = models.CharField(max_length=32)  # MD5 length is 32 symbols
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_cracked = models.BooleanField(default=False)
    cracked_password = models.CharField(max_length=5, blank=True, null=True) # due 5 symbols limit of password

    def __str__(self):
        return f"{self.md5_hash} by {self.user.username}"
