> [!CAUTION]
> This app alone is not meant to be used in production!

This is an example Django application that uses GCP Cloud KMS to 
take mock tokens and store it in an encrypted column of the database.

It currently uses symmetric encryption for each stored token.

# TODO
- Implement envelope encryption

# Getting Started

## 1. Setup GCP

You'll need the [gcloud](https://cloud.google.com/sdk/docs/install#mac) CLI installed on your system.

1. Create a GCP project.
2. Login with gcloud CLI: `gcloud auth login`
3. Set your project context: `gcloud config set-project <PROJECT ID>`
4. Enable the KMS API: `gcloud services enable cloudkms.googleapis.com`
5. Create the keyring: `gcloud kms keyrings create test-keyring --location global`
6. Create a key (this is using MacOS's version of `date`):

  ```sh
  gcloud kms keys create pat-encryption-key \
    --location global \
    --keyring test-keyring \
    --purpose encryption \
    --default-algorithm google-symmetric-encryption \
    --rotation-period "1d" \
    --next-rotation-time "$(date -u -v+1d +"%Y-%m-%dT%H:%M:%S.%4NZ")"
  ```
7. Login with application default credentials (just for testing!): `gcloud auth application-default login`

## 2. Setup Environment

1. Copy `.envrc.example` to `.envrc`: `cp .envrc .envrc.example`
2. Setup the environment variables in `.envrc`

  ```sh
  export GCP_PROJECT_ID="<YOUR PROJECT ID>"
  export KMS_LOCATION_ID="global"
  export KMS_KEY_RING_ID="test-keyring"
  export KMS_CRYPTO_KEY_ID="pat-encryption-key"
  ```
3. Install dependencies: `pip install -r requirements.txt`
4. Change directory into the Django project: `cd exampletink`
5. Setup the database (local SQLite DB): `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run devserver: `python manage.py runserver`
8. Access the app at: `http://127.0.0.1:8000/`
