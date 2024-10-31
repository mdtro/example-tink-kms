import os
from google.cloud import kms_v1
from tink import aead
from tink.integration import gcpkms

# Initialize Tink
aead.register()


def initialize_kms():
    kms_key_uri = (
        f"gcp-kms://projects/{os.getenv('GCP_PROJECT_ID')}/locations/"
        f"{os.getenv('KMS_LOCATION_ID')}/keyRings/{os.getenv('KMS_KEY_RING_ID')}/cryptoKeys/{os.getenv('KMS_CRYPTO_KEY_ID')}"
    )
    gcp_client = kms_v1.KeyManagementServiceClient()
    kms_aead = gcpkms.GcpKmsClient(kms_key_uri, gcp_client)

    return kms_aead.get_aead(kms_key_uri)


kms_aead = initialize_kms()
