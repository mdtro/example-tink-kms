from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from pats.models import UserGitHubToken
from pats.encryption import kms_aead


class Command(BaseCommand):
    help = "Re-encrypt GitHub PATs with the latest key version if older than a given number of days"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Re-encrypt tokens older than this many days",
        )

    def handle(self, *args, **options):
        days = options["days"]
        threshold_date = timezone.now() - timedelta(days=days)

        tokens_to_reencrypt = UserGitHubToken.objects.filter(
            last_encryption_date__lt=threshold_date
        )

        for token_entry in tokens_to_reencrypt:
            # Decrypt the current token
            current_token = token_entry.get_token()

            # Re-encrypt with the latest key version
            token_entry.set_token(current_token)
            token_entry.save()
            self.stdout.write(f"Re-encrypted token for user {token_entry.user.id}")

        self.stdout.write(f"Re-encryption completed for tokens older than {days} days.")
