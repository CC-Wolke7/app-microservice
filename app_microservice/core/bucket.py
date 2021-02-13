from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

from django.conf import settings

project_id = settings.GCP_PROJECT_ID
bucket_name = settings.GCP_BUCKET

client = storage.Client(
    project=project_id,
    credentials=AnonymousCredentials(),
)

bucket = client.bucket(bucket_name)

if not bucket.exists():
    bucket.create(client)


def download_image(name):
    blob = bucket.blob(name)
    image = blob.download_as_text()

    return image


def upload_image(name, image):
    blob = bucket.blob(name)
    blob.upload_from_string(image)
