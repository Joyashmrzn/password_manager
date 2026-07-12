from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet


def get_fernet():
    return Fernet(settings.FERNET_KEY.encode())


class VaultEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vault_entries')
    site_name = models.CharField(max_length=100)
    site_url = models.URLField(blank=True)
    site_username = models.CharField(max_length=150)
    encrypted_password = models.BinaryField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        f = get_fernet()
        self.encrypted_password = f.encrypt(raw_password.encode())

    def get_password(self):
        f = get_fernet()
        return f.decrypt(bytes(self.encrypted_password)).decode()

    def __str__(self):
        return f"{self.site_name} ({self.site_username})"