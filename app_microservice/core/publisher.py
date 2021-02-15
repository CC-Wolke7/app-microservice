import json
from uuid import UUID

# https://googleapis.dev/python/pubsub/latest/publisher/api/client.html
from google.cloud import pubsub_v1

from django.conf import settings

from core.serializers import OfferSerializer

project_id = settings.GCP_PROJECT_ID

# @TODO: fix for local testing
# https://github.com/googleapis/python-pubsub/issues?q=GOOGLE_APPLICATION_CREDENTIALS
publisher = pubsub_v1.PublisherClient()

new_offer_topic_path = publisher.topic_path(
    project_id, settings.RECOMMENDER_BOT_TOPIC
)


# https://stackoverflow.com/questions/36588126/uuid-is-not-json-serializable
def uuid_convert(o):
    if isinstance(o, UUID):
        return o.hex


def notify_offer_created(offer):
    serialized_payload = json.dumps(
        OfferSerializer(offer).data, default=uuid_convert
    ).encode('utf-8')

    try:
        future = publisher.publish(new_offer_topic_path, serialized_payload)
        future.result()

        print(
            f"Published 'newOffer' message to topic: '{new_offer_topic_path}'"
        )
    except Exception as e:
        print(f"Failed to publish 'newOffer' message: '{e}'")
