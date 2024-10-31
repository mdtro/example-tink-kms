from tink import aead
from tink.integration import gcpkms

from django.conf import settings

# Initialize Tink
aead.register()


def initialize_kms():
    kms_key_uri = f"gcp-kms://projects/{settings.GCP_PROJECT_ID}/locations/{settings.KMS_LOCATION_ID}/keyRings/{settings.KMS_KEY_RING_ID}/cryptoKeys/{settings.KMS_CRYPTO_KEY_ID}"
    kms_aead = gcpkms.GcpKmsClient(
        kms_key_uri, None
    )  # specifying None here forces application default creds

    return kms_aead.get_aead(kms_key_uri)


kms_aead = initialize_kms()
