from django.db import models
from django.utils import timezone

from .encryption import encrypt_token, decrypt_token


class UserGitHubToken(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    encrypted_token = models.BinaryField()
    last_encryption_date = models.DateTimeField(
        default=timezone.now
    )  # Track encryption date

    def set_token(self, token: str):
        self.encrypted_token = encrypt_token(token)
        self.last_encryption_date = timezone.now()

    def get_token(self) -> str:
        return decrypt_token(self.encrypted_token)
