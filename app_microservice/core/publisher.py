from google.cloud import pubsub_v1

from django.conf import settings


def create_topic(project_id, id):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")


def publish_messages(project_id, topic_id, data=dict(breed="schäferhund")):
    publisher = pubsub_v1.PublisherClient(credentials={})

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = data.encode("utf-8")

    # When you publish a message, the client returns a future.
    publisher.publish(topic_path, data)

    print(f"Published messages to {topic_path}.")


if __name__ == '__main__':
    project_id = settings.GCP_PROJECT_ID
    topic_id = settings.RECOMMENDER_BOT_TOPIC

    create_topic(project_id, topic_id)
    publish_messages(project_id, topic_id)
