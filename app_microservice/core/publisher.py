from google.auth import credentials
from google.cloud import pubsub_v1
import os


def create_topic(project_id, topic_id):
    """Create a new Pub/Sub topic."""
    # [START pubsub_quickstart_create_topic]
    # [START pubsub_create_topic]

    print(os.environ.get('PUBSUB_EMULATOR_HOST'))

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print("Created topic: {}".format(topic.name))
    # [END pubsub_quickstart_create_topic]
    # [END pubsub_create_topic]


def publish_messages(project_id, topic_id):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient(credentials={})
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data = '{ "breed": "schaeferhund" }'

    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)

    print(f"Published messages to {topic_path}.")
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]


if __name__ == '__main__':
    create_topic(project_id="vet-shelter", topic_id="recommend")
    publish_messages(project_id="vet-shelter", topic_id="recommend")