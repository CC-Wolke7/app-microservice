from django.core.management.base import BaseCommand

from core.publisher import new_offer_topic_path, publisher


class Command(BaseCommand):
    help = 'Create required topics on Google Cloud PubSub'

    def handle(self, *args, **options):
        publisher.create_topic(request={'name': new_offer_topic_path})
