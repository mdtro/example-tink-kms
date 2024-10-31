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

    kms_aead = kms_aead.get_aead(kms_key_uri)

    return aead.KmsEnvelopeAead(aead.aead_key_templates.AES256_GCM, kms_aead)


envelope_aead = initialize_kms()


def encrypt_token(token: str):
    # the value returned here is the ciphertext and encrypted DEK
    encrypted_token = envelope_aead.encrypt(token.encode("utf-8"), b"")
    return encrypted_token


def decrypt_token(encrypted_token):
    # Decrypt the token
    decrypted_token = envelope_aead.decrypt(encrypted_token, b"")
    return decrypted_token.decode("utf-8")
