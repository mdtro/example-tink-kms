from django.db import models
from django.utils import timezone

from .encryption import kms_aead


class UserGitHubToken(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    encrypted_token = models.BinaryField()
    last_encryption_date = models.DateTimeField(
        default=timezone.now
    )  # Track encryption date

    def set_token(self, token: str):
        self.encrypted_token = kms_aead.encrypt(token.encode("utf-8"), b"")
        self.last_encryption_date = timezone.now()

    def get_token(self) -> str:
        decrypted_token = kms_aead.decrypt(self.encrypted_token, b"")
        return decrypted_token.decode("utf-8")
