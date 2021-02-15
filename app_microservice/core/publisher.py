import json
from typing import TypedDict

from google.cloud import pubsub_v1

from django.conf import settings

project_id = settings.GCP_PROJECT_ID
topic_name = settings.RECOMMENDER_BOT_TOPIC

publisher = pubsub_v1.PublisherClient()


class OfferCreatedNotificationPayload(TypedDict):
    breed: str
    offer: str


def notify_offer_created(offer):
    topic_path = publisher.topic_path(project_id, topic_name)

    payload: OfferCreatedNotificationPayload = {
        'breed': offer.breed,
        'offer': str(offer.uuid)
    }

    serialized_payload = json.dumps(payload).encode('utf-8')

    try:
        future = publisher.publish(topic_path, serialized_payload)
        future.result()

        print(f"Published 'newOffer' message to topic: '{topic_path}'")
    except Exception as e:
        print(f"Failed to publish 'newOffer' message: '{e}'")
